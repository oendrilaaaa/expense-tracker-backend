from django.urls import path 
from .views import AuthView, login_api

urlpatterns = [
    path('auth/',AuthView.as_view()),
    path('login/', login_api, name='login'),
]