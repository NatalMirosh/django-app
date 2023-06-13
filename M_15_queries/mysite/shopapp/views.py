from timeit import default_timer

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .forms import ProductForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer

import logging

logger = logging.getLogger(__name__)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            logger.info('ShopIndexView: Get data shop-index')

            products = [
                ('Laptop', 1999),
                ('Desktop', 2999),
                ('Smartphone', 999),
            ]
            context = {
                "time_running": default_timer(),
                "products": products,
            }
            return render(request, 'shopapp/shop-index.html', context=context)
        except Exception as e:
            logger.error(f'ShopIndexView: Error: {str(e)}')
            return HttpResponse(status=500)


class ProductDetailsView(DetailView):
        template_name = "shopapp/products-details.html"
        # model = Product
        queryset = Product.objects.prefetch_related("images")
        context_object_name = "product"

        def get_context_data(self, **kwargs):
            try:
                context = super().get_context_data(**kwargs)
                product = self.object
                logger.info(f"ProductDetailsView: Viewing product details for '{product.name}'")
                return context

            except Product.DoesNotExist:
                raise Http404("Product does not exist")

            except Exception as e:
                logger.error(f"ProductDetailsView: Error: {str(e)}")
                raise


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            logger.info(f"ProductsListView: Viewing list products")
            return context

        except Exception as e:
            logger.error(f"ProductsListView: Error: {str(e)}")
            raise


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            logger.info("ProductCreateView: Creating new product")
            return response

        except Exception as e:
            logger.error(f"ProductCreateView: Error: {str(e)}")
            raise


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            logger.info(f"ProductUpdateView: Updating product with name {self.object.name}")

            for image in form.files.getlist("images"):
                ProductImage.objects.create(
                    product=self.object,
                    image=image,
                )
            return response

        except Exception as e:
            logger.error(f"ProductUpdateView: Error updating product: {str(e)}")
            raise


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        try:
            self.object = self.get_object()
            logger.info(f"ProductDeleteView: Deleting product with name {self.object.name}")

            success_url = self.get_success_url()
            self.object.archived = True
            self.object.save()
            return HttpResponseRedirect(success_url)
        except Exception as e:
            logger.error(f"ProductDeleteView: Error deleting  product: {str(e)}")
            raise


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

    def get(self, request, *args, **kwargs):
        try:
            logger.info(f"OrdersListView: Viewing list orders")
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"OrdersListView: Error: {str(e)}")
            raise


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            logger.info(f"OrderDetailView: Viewing detail order {self.object.pk}")
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"OrderDetailView: Error: {str(e)}")
            raise


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})
