from random import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from home.forms import CustomUserForm, CustomUserUpdateForm, PlayerSelectionForm
from home.models import CustomUserModel, TeamModel, ChoseTeamModel, SelectedPlayer
import random


@login_required
def choose_team(request):
    chosen_team = ChoseTeamModel.objects.get(user=request.user)
    selected_players = SelectedPlayer.objects.filter(user=request.user)

    # Get the new team from the form
    if request.method == 'POST':
        new_team_id = request.POST.get('team_id')
        new_team = TeamModel.objects.get(id=new_team_id)

        # Check if the team has changed
        if chosen_team.team != new_team:
            # Clear previously selected players
            SelectedPlayer.objects.filter(user=request.user).delete()

            # Optionally, update the chosen team
            chosen_team.team = new_team
            chosen_team.save()

        # Redirect or render the page as necessary
        return redirect('select_players')  # Or wherever you want to go next

    return render(request, 'pages/choose_team.html', {'teams': TeamModel.objects.all()})


@login_required
def select_players(request):
    chosen_team = ChoseTeamModel.objects.get(user=request.user)
    selected_players = SelectedPlayer.objects.filter(user=request.user)

    if request.method == 'POST':
        form = PlayerSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            SelectedPlayer.objects.filter(user=request.user).delete()
            players = form.cleaned_data['players']
            for player in players:
                SelectedPlayer.objects.create(user=request.user, player=player)
            return redirect('home_page')
    else:
        form = PlayerSelectionForm(user=request.user)

    return render(request, 'pages/select_players.html', {'form': form})

@login_required
def chosen_players(request):
    selected_players = SelectedPlayer.objects.filter(user=request.user)

    return render(request, 'pages/chosen_players.html', {'selected_players': selected_players})



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
