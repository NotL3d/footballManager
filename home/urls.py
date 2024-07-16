from django.urls import path
from home import views
from home.views import choose_team

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


]
