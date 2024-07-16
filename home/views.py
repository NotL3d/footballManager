from random import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView

from home.forms import CustomUserForm, CustomUserUpdateForm
from home.models import CustomUserModel, TeamModel, ChoseTeamModel



@login_required
def choose_team(request):
    # Retrieve or create the user's team selection instance
    chosen_team, created = ChoseTeamModel.objects.get_or_create(user=request.user)

    if request.method == "POST":
        team_id = request.POST.get('team_id')

        if not team_id:
            return render(request, 'pages/choose_team.html',
                          {'teams': TeamModel.objects.all(), 'error': 'No team ID provided'})

        try:
            team = TeamModel.objects.get(id=team_id)
            chosen_team.team = team  # Update team if found
            chosen_team.save()
            return render(request, 'pages/home.html')
        except TeamModel.DoesNotExist:
            return render(request, 'pages/choose_team.html',
                          {'teams': TeamModel.objects.all(), 'error': 'Team not found'})

    return render(request, 'pages/choose_team.html', {'teams': TeamModel.objects.all(), 'chosen_team': chosen_team})



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

