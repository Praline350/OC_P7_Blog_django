from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View

from authentication.models import User
from authentication.forms import LoginForm, SignUpForm, UploadProfilePhotoForm
from blog.models import Ticket, Review, UserFollows, UserBlock


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


class UploadProfilePhotoView(View):
    template_name = 'authentication/upload_profile_photo.html'
    form_class = UploadProfilePhotoForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect_url': reverse('profile')})
        return JsonResponse({'success': False, 'error': form.errors.as_json()})


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


class ProfilePageView(LoginRequiredMixin, View):
    template_name = 'authentication/profile.html'
    form_class = UploadProfilePhotoForm

    def get(self, request):
        user = request.user
        form = self.form_class(instance=user)
        tickets = Ticket.objects.filter(user=user)
        reviews = Review.objects.filter(user=user)
        tickets_count = tickets.count()
        reviews_count = reviews.count()
        following_ids = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
        follows_users = User.objects.filter(id__in=following_ids)
        follower_ids = UserFollows.objects.filter(followed_user=request.user).values_list('user_id', flat=True)

        # Obtenir les IDs des utilisateurs bloqués
        blocked_user_ids = UserBlock.objects.filter(user=request.user).values_list('blocked_user_id', flat=True)
        
        following_count = UserFollows.objects.filter(user=user).count()
        followers_count = UserFollows.objects.filter(followed_user=user).count()
        star_range = range(1, 6)
        context = {
            'form': form,
            'user': user,
            'tickets': tickets,
            'reviews': reviews,
            'tickets_count': tickets_count,
            'reviews_count': reviews_count,
            "star_range": star_range,
            'following_ids': following_ids,  # Passez les IDs des utilisateurs suivis
            'follower_ids': follower_ids,  # Passez les IDs des utilisateurs qui suivent l'utilisateur connecté
            'blocked_user_ids': blocked_user_ids,  # Passez les IDs des utilisateurs bloqués
            'following_count': following_count,
            'followers_count': followers_count,
            'follows_users': follows_users,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'authentication/user_profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        tickets_count = Ticket.objects.filter(user=user).count()
        tickets = Ticket.objects.filter(user=user)
        reviews = Review.objects.filter(user=user)
        tickets_count = tickets.count()
        reviews_count = reviews.count()
        following_ids = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
        follows_ids = UserFollows.objects.filter(user=user).values_list('followed_user_id', flat=True)
        follows_users = User.objects.filter(id__in=follows_ids)
        follower_ids = UserFollows.objects.filter(followed_user=request.user).values_list('user_id', flat=True)

        # Obtenir les IDs des utilisateurs bloqués
        blocked_user_ids = UserBlock.objects.filter(user=request.user).values_list('blocked_user_id', flat=True)
        
        following_count = UserFollows.objects.filter(user=user).count()
        followers_count = UserFollows.objects.filter(followed_user=user).count()
        star_range = range(1, 6)
        context = {
            'user': user,
            'tickets': tickets,
            'reviews': reviews,
            'tickets_count': tickets_count,
            'reviews_count': reviews_count,
            'following_ids': following_ids,  # Passez les IDs des utilisateurs suivis
            'follower_ids': follower_ids,  # Passez les IDs des utilisateurs qui suivent l'utilisateur connecté
            'blocked_user_ids': blocked_user_ids,  # Passez les IDs des utilisateurs bloqués
            'following_count': following_count,
            'followers_count': followers_count,
            "star_range": star_range,
            "follows_users" : follows_users

        }
        return render(request, self.template_name, context)