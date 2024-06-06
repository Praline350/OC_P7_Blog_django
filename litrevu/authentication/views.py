from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View

from authentication.forms import LoginForm, SignUpForm, UploadProfilePhotoForm

class LoginPageView(View):
    template_name = 'authentication/login.html'
    login_form_class = LoginForm
    signup_form_class = SignUpForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        login_form = self.login_form_class()
        signup_form = self.signup_form_class()
        context = {
            'login_form': login_form,
            'signup_form': signup_form,
        }
        return render(request, self.template_name, context=context)
        
    def post(self, request):
        login_form = self.login_form_class(request.POST)
        signup_form = self.signup_form_class(request.POST)
        if 'login_form' in request.POST:
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['login_username'],
                    password=login_form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Identifiants Invalides')
        if 'signup_form' in request.POST:
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'Erreur d\'inscription')
        context = {
            'login_form': login_form,
            'signup_form': signup_form,
        }
        return render(request, self.template_name, context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


def upload_profile_photo(request):
    form = UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'authentication/change_password.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, pour que l'utilisateur ne soit pas déconnecté
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
        return render(request, self.template_name, {'form': form})
