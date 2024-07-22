from django.urls import path
from home import views
from home.views import choose_team, select_players, choosen_players

urlpatterns = [
    # home path
    path('', views.HomePageView.as_view(), name='home_page'),
    # user paths
    path('register-user/', views.UserCreateView.as_view(), name='register_user'),
    path('update-user/<int:pk>/', views.UserUpdateView.as_view(), name='update_user'),
    path('delete-user/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('view-user/<int:pk>', views.UserDetailView.as_view(), name='detail_user'),
    # choose team path
    path('choose_team/', choose_team, name='choose_team'),
    path('select_players/', select_players, name='select_players'),
    path('chosen-players/', choosen_players, name='chosen_players'),
    # play path
    path('start-tournament/', views.start_tournament, name='start_tournament'),
    path('tournament-stage/', views.tournament_stage, name='tournament_stage'),
    # path to all users
    path('list_of_users/', views.UserListView.as_view(), name='list_of_users'),
    #play with user path
    path('play_with_another_user/', views.play_with_another_user, name='play_with_another_user'),
    path('simulate_user_vs_user/<int:opponent_id>', views.simulate_user_vs_user, name='simulate_user_vs_user'),

]
