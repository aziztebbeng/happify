from django.urls import path
from django.contrib.auth import views as auth_views
from happifyapp import views

urlpatterns = [
    path('login/', views.login, name='login'),  
    path('signup/', views.signup, name='signup'),
    path('preferences/', views.preferences, name='preferences'),
    path('homepage/', views.homepage, name='homepage'),
]

