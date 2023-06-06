from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from django.views.generic import DetailView

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView

from shopapp.models import ProductImage
from .forms import AvatarUploadForm
from .models import Profile


class UserListView(ListView):
    model = User
    template_name = 'myauth/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'myauth/user_detail.html'
    context_object_name = 'user'

    @method_decorator(staff_member_required, name='post')
    def post(self, request, *args, **kwargs):
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = self.get_object()
            avatar = form.cleaned_data['avatar']
            if request.user.is_staff:
                user.profile.avatar = avatar
                user.profile.save()
        return redirect('myauth:user-detail', pk=user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AvatarUploadForm()
        return context


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        context['user'] = self.request.user
        context['profile'] = profile
        return context

    def get(self, request):
        form = AvatarUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data['avatar']
            profile, created = Profile.objects.get_or_create(user=self.request.user)
            profile.avatar = avatar
            profile.save()
            return render(request, self.template_name, {'form': form, 'success_message': 'Avatar uploaded successfully'})
        else:
            return render(request, self.template_name, {'form': form})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
