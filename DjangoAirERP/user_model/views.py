from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.views import View
from .utils import send_email_for_confirm
from .forms import UserForm
from .models import User


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={}, status=200)
            return JsonResponse(data={'error': 'Password or login is not valid'}, status=400)
        return JsonResponse(data={'error': 'Enter your username and password'}, status=400)


class SignUp(View):
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            send_email_for_confirm(request, user)
            return JsonResponse(data={}, status=200)
        return JsonResponse(
            data={'error': [error.title() for error in form.errors]},
            status=400)


class EmailVerify(View):
    @staticmethod
    def get_user(uidb64):
        """User search by uidb64"""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def get(self, request, uidb64, token):
        """Check the token for a match, save the check and redirect to the home page"""
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            return redirect('index')
        return redirect('invalid_verify')
