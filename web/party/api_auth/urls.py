from django.urls import path

from .views import *

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('register', RegisterView.as_view()),
    path('users/activate', ActivateAccountView.as_view()),
    path('users/resend_activation_code', ResendActivationCodeView.as_view())
]
