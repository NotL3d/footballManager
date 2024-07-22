from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, ListView
from home.forms import CustomUserForm, CustomUserUpdateForm, PlayerSelectionForm
from home.models import CustomUserModel, TeamModel, ChooseTeamModel, SelectedPlayer, Player
import random


# login_required decorator to restrict access only to authenticated users
@login_required
def choose_team(request):
    try:
        chosen_team = ChooseTeamModel.objects.get(user=request.user)
        team_chosen = True
    except ChooseTeamModel.DoesNotExist:
        chosen_team = None
        team_chosen = False

    # Get the new team from the form
    if request.method == 'POST':
        new_team_id = request.POST.get('team_id')
        new_team = TeamModel.objects.get(id=new_team_id)

        if chosen_team is None:
            # Create a new ChoseTeamModel entry
            chosen_team = ChooseTeamModel.objects.create(user=request.user, team=new_team)
        elif chosen_team.team != new_team:
            # Clear previously selected players
            SelectedPlayer.objects.filter(user=request.user).delete()

            # Update the chosen team
            chosen_team.team = new_team
            chosen_team.save()

        return redirect('select_players')  # Or wherever you want to go next

    context = {
        'teams': TeamModel.objects.all(),
        'chosen_team': chosen_team.team if chosen_team else None,  # Ensure you're accessing the team attribute
        'team_chosen': team_chosen,
    }

    return render(request, 'pages/choose_team.html', context)


@login_required
def select_players(request):
    chosen_team = ChooseTeamModel.objects.get(user=request.user)
    selected_players = SelectedPlayer.objects.filter(user=request.user)

    if request.method == 'POST':
        form = PlayerSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            # Clear existing selected players for the user
            SelectedPlayer.objects.filter(user=request.user).delete()

            # Save the selected players from the form
            goalkeeper = form.cleaned_data['goalkeeper']
            attacker = form.cleaned_data['attacker_1']
            attacker_2 = form.cleaned_data['attacker_2']
            defender = form.cleaned_data['defender']
            defender_2 = form.cleaned_data['defender_2']
            defender_3 = form.cleaned_data['defender_3']
            defender_4 = form.cleaned_data['defender_4']
            midfielder = form.cleaned_data['midfielder']
            midfielder_2 = form.cleaned_data['midfielder_2']
            midfielder_3 = form.cleaned_data['midfielder_3']
            midfielder_4 = form.cleaned_data['midfielder_4']

            SelectedPlayer.objects.create(user=request.user, player=goalkeeper)
            SelectedPlayer.objects.create(user=request.user, player=attacker)
            SelectedPlayer.objects.create(user=request.user, player=attacker_2)
            SelectedPlayer.objects.create(user=request.user, player=defender)
            SelectedPlayer.objects.create(user=request.user, player=defender_2)
            SelectedPlayer.objects.create(user=request.user, player=defender_3)
            SelectedPlayer.objects.create(user=request.user, player=defender_4)
            SelectedPlayer.objects.create(user=request.user, player=midfielder)
            SelectedPlayer.objects.create(user=request.user, player=midfielder_2)
            SelectedPlayer.objects.create(user=request.user, player=midfielder_3)
            SelectedPlayer.objects.create(user=request.user, player=midfielder_4)

            # Redirect to home_page upon successful form submission
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
    return ChooseTeamModel.objects.get(user=user).team


def compute_team_score(team, user_team, user):
    if user_team == team:
        players = [sp.player for sp in SelectedPlayer.objects.filter(user=user)]
    else:
        all_players = list(Player.objects.filter(team=team))
        players = random.sample(all_players, min(11, len(all_players)))  # Select 11 or fewer if less than 11 players

    score = sum(player.ball_skills + player.passing + player.shooting + player.defence +
                player.physical + player.mental + player.goalkeeper for player in players)


    score = round(score / 1100)
    return score, len(players)


def simulate_match(team1, team2, user_team, user):
    score1, num_players_team1 = compute_team_score(team1, user_team, user)
    score2, num_players_team2 = compute_team_score(team2, user_team, user)

    # Adjusting the random score modification to be more balanced
    score1 += random.randint(-2, 2)
    score2 += random.randint(-2, 2)

    # Ensure scores are non-negative
    score1 = max(score1, 0)
    score2 = max(score2, 0)

    return score1, num_players_team1, score2, num_players_team2


def simulate_stage(teams, user_team, user):
    matches = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]
    winners = []
    results = []
    user_won = False

    for team1, team2 in matches:
        score1, num_players_team1, score2, num_players_team2 = simulate_match(team1, team2, user_team, user)

        if team1 == user_team or team2 == user_team:
            if (team1 == user_team and score1 > score2) or (team2 == user_team and score2 > score1):
                winners.append(user_team)
                user_won = True
            else:
                user.losses += 1
                user.save()
        else:
            if score1 > score2:
                winners.append(team1)
            else:
                winners.append(team2)

        results.append({
            'team_1': team1,
            'team_2': team2,
            'score_team_1': score1,
            'score_team_2': score2,
            'num_players_team1': num_players_team1,
            'num_players_team2': num_players_team2
        })

    if user_won:
        user.wins += 1
        user.save()

    return winners, user_won, results


@login_required
def start_tournament(request):
    user_team = get_user_team(request.user)
    all_teams = list(TeamModel.objects.exclude(id=user_team.id))
    random.shuffle(all_teams)
    computer_team = all_teams.pop()  # Choose a computer team
    tournament_teams = [user_team, computer_team] + all_teams[:14]  # Total 16 teams

    request.session['tournament_teams'] = [team.id for team in tournament_teams]
    request.session['current_stage'] = 'Primele 16 echipe'

    # Pass the computer_team to the template
    context = {
        'user_team': user_team,
        'computer_team': computer_team,
        'tournament_teams': tournament_teams,
    }

    return redirect('tournament_stage')


def tournament_stage(request):
    user_team = get_user_team(request.user)
    teams = TeamModel.objects.filter(id__in=request.session['tournament_teams'])
    stage = request.session['current_stage']

    # Initialize results to avoid reference before assignment
    results = []

    if stage == 'Primele 16 echipe':
        winners, user_won, results = simulate_stage(teams, user_team, request.user)
        if not user_won:
            messages.error(request, "Din păcate ai pierdut!")
            return redirect('start_tournament')
        request.session['tournament_teams'] = [team.id for team in winners]
        request.session['current_stage'] = 'Sferturi de finală'

    elif stage == 'Sferturi de finală':
        winners, user_won, results = simulate_stage(teams, user_team, request.user)
        if not user_won:
            messages.error(request, "Din păcate ai pierdut!")
            return redirect('start_tournament')
        request.session['tournament_teams'] = [team.id for team in winners]
        request.session['current_stage'] = 'Semifinale'

    elif stage == 'Semifinale':
        winners, user_won, results = simulate_stage(teams, user_team, request.user)
        if not user_won:
            messages.error(request, "Din păcate ai pierdut!")
            return redirect('start_tournament')
        request.session['tournament_teams'] = [team.id for team in winners]
        request.session['current_stage'] = 'Finala'

    elif stage == 'Finala':
        winners, user_won, results = simulate_stage(teams, user_team, request.user)
        if not user_won:
            messages.error(request, "Din păcate ai pierdut!")
            return redirect('start_tournament')
        champion = winners[0]
        request.session['tournament_teams'] = [champion.id]
        request.session['current_stage'] = 'Campioana!'
        return render(request, 'pages/result_game_computer.html',
                      {'stage': stage, 'teams': teams, 'Campioana!': user_team, 'results': results})

    return render(request, 'pages/result_game_computer.html', {'stage': stage, 'teams': teams,
                                                               'user_team': user_team, 'results': results})


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


# view list of users

class UserListView(ListView):
    template_name = 'pages/play_with_another_user.html'
    model = CustomUserModel
    context_object_name = 'all_users'

    def get_queryset(self):
        return CustomUserModel.objects.exclude(id=self.request.user.id)


@login_required
def play_with_another_user(request):
    users = CustomUserModel.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        opponent_id = request.POST.get('opponent')
        if opponent_id:
            return redirect('simulate_user_vs_user', opponent_id=opponent_id)
    return render(request, 'pages/play_with_another_user.html', {'users': users})


def simulate_match_user(team1, team2):
    # Example simulation logic based on player attributes
    team1_score = sum(player.overall_avg for player in team1.player_set.all()) // 1100
    team2_score = sum(player.overall_avg for player in team2.player_set.all()) // 1100

    # Add some randomness
    team1_score += random.randint(0, 5)
    team2_score += random.randint(0, 5)

    return team1_score, team2_score


@login_required
def simulate_user_vs_user(request, opponent_id):
    CustomUserModel = get_user_model()
    user = get_object_or_404(CustomUserModel, pk=request.user.id)
    user_team = get_object_or_404(TeamModel, choseteammodel__user=user)
    opponent = get_object_or_404(CustomUserModel, pk=opponent_id)
    opponent_team = get_object_or_404(TeamModel, choseteammodel__user=opponent)

    # Simulate the match
    user_score, opponent_score = simulate_match_user(user_team, opponent_team)

    # Update user stats
    if user_score > opponent_score:
        user.wins += 1
        opponent.losses += 1
        user_won = True
    elif user_score < opponent_score:
        user.losses += 1
        opponent.wins += 1
        user_won = False
    else:
        user_won = None  # It's a draw, handle accordingly if needed

    user.save()
    opponent.save()

    return render(request, 'pages/match_result.html', {
        'user_team': user_team,
        'opponent_team': opponent_team,
        'user_score': user_score,
        'opponent_score': opponent_score,
        'user_won': user_won
    })
