from django.urls import path
from home import views
from home.views import choose_team, select_players, chosen_players

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
    path('chosen-players/', chosen_players, name='chosen_players'),
    # play path
    path('start-tournament/', views.start_tournament, name='start_tournament'),
    path('tournament-stage/', views.tournament_stage, name='tournament_stage'),
]
