from django.urls import path
from django.views.generic import TemplateView
from .views import SignUp, Login, EmailVerify

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("signup/", SignUp.as_view(), name="signup"),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='email_verify/invalid_verify.html'),
         name='invalid_verify'),
]
