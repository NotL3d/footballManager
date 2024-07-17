from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from home.forms import CustomUserForm, CustomUserUpdateForm, PlayerSelectionForm
from home.models import CustomUserModel, TeamModel, ChoseTeamModel, SelectedPlayer, Player
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

# game loop

def get_user_team(user):
    return ChoseTeamModel.objects.get(user=user).team

def compute_team_score(team):
    players = Player.objects.filter(team=team)
    score = 0
    for player in players:
            score += player.ball_skills + player.passing + player.shooting + player.defence + player.physical + player.mental + player.goalkeeper
    return score

def simulate_match(team1, team2):
    score1 = compute_team_score(team1) + random.randint(-10, 10)
    score2 = compute_team_score(team2) + random.randint(-10, 10)
    return score1, score2


def simulate_stage(teams, user_team):
    matches = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]
    winners = []
    user_won = False

    for team1, team2 in matches:
        score1, score2 = simulate_match(team1, team2)
        if team1 == user_team or team2 == user_team:
            if (team1 == user_team and score1 > score2) or (team2 == user_team and score2 > score1):
                winners.append(user_team)
                user_won = True
            else:
                return None, False  # User lost
        else:
            if score1 > score2:
                winners.append(team1)
            else:
                winners.append(team2)

    return winners, user_won

def start_tournament(request):
    user_team = get_user_team(request.user)
    all_teams = list(TeamModel.objects.exclude(id=user_team.id))
    random.shuffle(all_teams)
    computer_team = all_teams.pop()  # Choose a computer team
    tournament_teams = [user_team, computer_team] + all_teams[:14]  # Total 16 teams
    request.session['tournament_teams'] = [team.id for team in tournament_teams]
    request.session['current_stage'] = 'Round of 16'
    return redirect('tournament_stage')


def tournament_stage(request):
    user_team = get_user_team(request.user)
    teams = TeamModel.objects.filter(id__in=request.session['tournament_teams'])
    stage = request.session['current_stage']

    if stage == 'Round of 16':
        winners, user_won = simulate_stage(teams, user_team)
        if not user_won:
            messages.error(request, "You lost! Game over.")
            return redirect('start_tournament')
        request.session['tournament_teams'] = [team.id for team in winners]
        request.session['current_stage'] = 'Quarterfinals'

    elif stage == 'Quarterfinals':
        winners, user_won = simulate_stage(teams, user_team)
        if not user_won:
            messages.error(request, "You lost! Game over.")
            return redirect('start_tournament')
        request.session['tournament_teams'] = [team.id for team in winners]
        request.session['current_stage'] = 'Semifinals'

    elif stage == 'Semifinals':
        winners, user_won = simulate_stage(teams, user_team)
        if not user_won:
            messages.error(request, "You lost! Game over.")
            return redirect('start_tournament')
        request.session['tournament_teams'] = [team.id for team in winners]
        request.session['current_stage'] = 'Final'

    elif stage == 'Final':
        winners, user_won = simulate_stage(teams, user_team)
        if not user_won:
            messages.error(request, "You lost! Game over.")
            return redirect('start_tournament')
        champion = winners[0]
        request.session['tournament_teams'] = [champion.id]
        request.session['current_stage'] = 'Champion'
        return render(request, 'pages/result_game_computer.html', {'stage': stage, 'teams': teams, 'champion': champion})

    return render(request, 'pages/result_game_computer.html', {'stage': stage, 'teams': teams,
                                                               'user_team': user_team})





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
