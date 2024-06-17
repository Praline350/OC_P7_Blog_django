import os
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from dotenv import load_dotenv
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import View
import requests
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from authentication.models import User
from blog.models import Ticket, Image, Review, UserFollows, UserBlock
from blog.forms import TicketForm, TicketEditForm, ImageForm, ReviewForm, ReviewEditForm, TicketReviewForm, UserSearchForm

load_dotenv()


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'blog/home.html'

    def get(self, request):
        blocked_users = UserBlock.objects.filter(user=request.user).values_list('blocked_user', flat=True)
        tickets = Ticket.objects.filter().exclude(user__id__in=blocked_users).order_by('-time_created')  
        reviews = Review.objects.filter().exclude(user__id__in=blocked_users).order_by('-time_created')
        following_ids = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
        following = User.objects.filter(id__in=following_ids)
        followed_by_ids = UserFollows.objects.filter(followed_user=request.user).values_list('user', flat=True)
        followed_by = User.objects.filter(id__in=followed_by_ids)
        combined_ids = list(following_ids) + list(followed_by_ids)
        combined_users = User.objects.filter(id__in=combined_ids)
        follows_tickets = Ticket.objects.filter(user__in=combined_users).exclude(user__id__in=blocked_users).order_by('-time_created')
        users = User.objects.exclude(username=request.user.username).exclude(id__in=blocked_users)
        star_range = range(1, 6)
        context = {
            "users": users,
            "tickets": tickets,
            "reviews": reviews,
            "star_range": star_range,
            'following': following,
            "followed_by": followed_by,
            'follows_tickets': follows_tickets,
        }
        return render(request, self.template_name, context)
    

class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow != request.user:
            _, created = UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
            if created:
                messages.success(request, f'Vous suivez maintenant {user_to_follow.username}.')
            else:
                messages.info(request, f'Vous suivez déjà {user_to_follow.username}.')
        return redirect('user_profile', username=username)
    

class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_unfollow = get_object_or_404(User, username=username)
        if user_to_unfollow != request.user:
            UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
            messages.success(request, f'Vous ne suivez plus {user_to_unfollow.username}.')
        return redirect('user_profile', username=username)


class TicketUploadView(LoginRequiredMixin, View):
    template_name = "blog/ticket_upload.html"
    ticket_form_class = TicketForm
    image_form_class = ImageForm

    def get(self, request):
        ticket_form = self.ticket_form_class()
        image_form = self.image_form_class()
        context = {
            "image_form": image_form,
            "ticket_form": ticket_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.ticket_form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            image_url = request.POST.get('image_url')
            if image_url:
                image_content = download_image(image_url)
                if image_content:
                    ticket.image.save(f'{ticket.title}.jpg', image_content, save=False)
            ticket.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class TicketEditView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketEditForm
    template_name = "blog/ticket_edit.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "blog/ticket_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ReviewUploadView(LoginRequiredMixin, View):
    template_name = "blog/review_upload.html"
    form_class = ReviewForm

    def get(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        form = self.form_class(ticket=ticket)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        form = self.form_class(request.POST, ticket=ticket)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
        return render(request, self.template_name, context={"form": form})
    

class ReviewEditView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewEditForm
    template_name = "blog/review_edit.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "blog/review_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    

class CreateTicketReviewView(LoginRequiredMixin, View):
    template_name = 'blog/create_ticket_review.html'
    form_class = TicketReviewForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                user=request.user
            )
            ticket.save()
            image_url = request.POST.get('image_url')
            if image_url:
                image_content = download_image(image_url)
                if image_content:
                    ticket.image.save(f'{ticket.title}.jpg', image_content, save=False)
                    ticket.save() 
            
            review = Review(
                headline=form.cleaned_data['review_headline'],
                body=form.cleaned_data['review_body'],
                rating=form.cleaned_data['review_rating'],
                ticket=ticket,
                user=request.user
            )
            review.save()

            return redirect('home')  # Redirigez vers la page d'accueil ou une autre page après la création
        return render(request, self.template_name, {'form': form})


class BlockUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_block = get_object_or_404(User, username=username)
        UserBlock.objects.get_or_create(user=request.user, blocked_user=user_to_block)
        UserFollows.objects.filter(user=request.user, followed_user=user_to_block).delete()
        UserFollows.objects.filter(user=user_to_block, followed_user=request.user).delete()
        messages.success(request, f'Vous avez bloqué {user_to_block.username}.')
        return redirect('user_profile', username=username)

class UnblockUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_unblock = get_object_or_404(User, username=username)
        UserBlock.objects.filter(user=request.user, blocked_user=user_to_unblock).delete()
        messages.success(request, f'Vous avez débloqué {user_to_unblock.username}.')
        return redirect('user_profile', username=username)


def search_users(request):
   
    
    form = UserSearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    return render(request, 'blog/search_users.html', {'form': form, 'query': query, 'results': results})


class APIFetcher:
    def __init__(self):
        self.url = 'https://www.googleapis.com/books/v1/volumes'
        self.key = os.getenv('API_KEY')

    def get_books(self, query):
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {
            'key': self.key,  # Remplace cette valeur par ta propre clé d'API
            'q': query,
            'maxResults': 10
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        return None


def search_books_api(request):
    query = request.GET.get('query', '')
    fetcher = APIFetcher()
    books = fetcher.get_books(query)
    book_list = []
    for book in books:
        volume_info = book.get('volumeInfo', {})
        title = volume_info.get('title', 'Titre inconnu')
        authors = ', '.join(volume_info.get('authors', ['Auteur inconnu']))
        image = volume_info.get('imageLinks', {}).get('thumbnail', '')
        book_list.append({'title': title, 'authors': authors, 'image': image})
    return JsonResponse({'books': book_list})


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None
