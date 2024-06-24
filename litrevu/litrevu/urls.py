"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
import authentication.views
import blog.views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('change_password/', authentication.views.ChangePasswordView.as_view(),
         name='password_change'),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('delete-account/', authentication.views.delete_account, name='delete_account'),

    # Profiles
    path('profile-photo/upload', authentication.views.UploadProfilePhotoView.as_view(),
         name='upload_profile_photo'),
    path('profile/', authentication.views.ProfilePageView.as_view(), name='profile'),
    path('profile/<str:username>/', authentication.views.UserProfileView.as_view(), name='user_profile'),

    # Blog URLs
    path('home/', blog.views.HomeView.as_view(), name='home'),
    path('blog/ticket_upload/', blog.views.TicketUploadView.as_view(), name='ticket_upload'),
    path('blog/ticket/<int:pk>/edit/', blog.views.TicketEditView.as_view(), name='ticket_edit'),
    path('blog/ticket/<int:pk>/delete', blog.views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('blog/ticket/<int:pk>/review_upload/', blog.views.ReviewUploadView.as_view(), name='review_upload'),
    path('blog/create-review/', blog.views.CreateTicketReviewView.as_view(), name='create_ticket_review'),
    path('blog/review/<int:pk>/edit/', blog.views.ReviewEditView.as_view(), name='review_edit'),
    path('blog/review/<int:pk>/delete/', blog.views.ReviewDeleteView.as_view(), name='review_delete'),

    # User follow/block
    path('block_user/<str:username>/', blog.views.BlockUserView.as_view(), name='block_user'),
    path('unblock_user/<str:username>/', blog.views.UnblockUserView.as_view(), name='unblock_user'),
    path('user/<str:username>/follow/', blog.views.FollowUserView.as_view(), name='follow_user'),
    path('user/<str:username>/unfollow/', blog.views.UnfollowUserView.as_view(), name='unfollow_user'),

    # API endpoint for book search
    path('search_user/', blog.views.search_users, name='search_users'),

    # User search
    path('search-books-api/', blog.views.search_books_api, name='search_books_api'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    

