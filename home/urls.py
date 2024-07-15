from django.urls import path
from home import views

urlpatterns = [

    path('', views.HomePageView.as_view(), name='home_page'),
    path('register-user/', views.UserCreateView.as_view(), name='register_user'),

]
