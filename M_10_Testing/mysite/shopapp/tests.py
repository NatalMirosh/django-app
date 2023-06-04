from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User, Permission
from shopapp.utils import add_two_numbers
from string import ascii_letters
from random import choices

from shopapp.models import Product, Order


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        # products =  Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='bob', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        #self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_get_products(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='bob', password='qwerty')
        view_order_permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(view_order_permission)
        cls.product = Product.objects.create(name='Banana', price=350)
        cls.order = Order.objects.create(delivery_address='Test Address', promocode='TEST123', user=cls.user)
        cls.order.products.add(cls.product)

    def setUp(self):
        self.client = Client()
        self.client.login(username='bob', password='qwerty')

    def test_order_details(self):
        url = reverse('shopapp:order_details', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)
        self.assertEqual(response.context['order'].products.first(), self.product)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls.product.delete()
        cls.order.delete()
        cls.user.delete()



# class OrdersExportTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='admin', password='admin123')
#         cls.user.is_staff = True
#         cls.user.save()
#
#     def setUp(self):
#         self.client = Client()
#         self.client.login(username='admin', password='admin123')
#
#     def tearDown(self):
#         self.client.logout()
#
#     def test_orders_export(self):
#         url = reverse('shopapp:orders_export')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response['Content-Type'], 'application/json')
#         self.assertIn('orders', response.json())
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.user.delete()
#         super().tearDownClass()


class OrdersExportTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'orders-fixture.json',
        'users-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='admin', password='admin123')
        cls.user.is_staff = True
        cls.user.save()

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def tearDown(self):
        self.client.logout()

    def test_orders_export(self):
        url = reverse('shopapp:orders_export')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('orders', response.json())

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.groups.clear()
        cls.user.delete()
