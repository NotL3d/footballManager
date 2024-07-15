from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from home.forms import CustomUserForm
from home.models import CustomUserModel


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'pages/home.html'





class UserCreateView(CreateView):
    template_name = 'registration/user/create_user.html'
    model = CustomUserModel
    form_class = CustomUserForm
    success_url = reverse_lazy('home_page')  # de adaugat chose team if not chosen


