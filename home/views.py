from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView

from home.forms import CustomUserForm, CustomUserUpdateForm
from home.models import CustomUserModel


# home view
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


# view for user registration
class UserCreateView(CreateView):
    template_name = 'registration/user/create_user.html'
    model = CustomUserModel
    form_class = CustomUserForm
    success_url = reverse_lazy('home_page')  # de adaugat chose team if not chosen


# view for update an existing account
class UserUpdateView(UpdateView):
    template_name = 'registration/user/update_user.html'
    model = CustomUserModel
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('home_page')


# view for detail of an existing account
class UserDetailView(DetailView):
    template_name = 'registration/user/detail_user.html'
    model = CustomUserModel
    context_object_name = 'user_profile'


# view for deleting user account
class UserDeleteView(DeleteView):
    template_name = 'registration/user/delete_user.html'
    model = CustomUserModel
    success_url = reverse_lazy('home_page')

