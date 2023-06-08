from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import CreationForm, CustomAuthenticationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('checker:file_upload')
    template_name = 'users/signup.html'


class CustomLogin(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')