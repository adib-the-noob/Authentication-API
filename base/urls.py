from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.UserRegistration.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('change-password/',views.UserChangePassword.as_view(),name='change-password'),
    path('send-reset-password-email/',views.SendPasswordResetEmail.as_view(),name='send-reset-password-email'),
]