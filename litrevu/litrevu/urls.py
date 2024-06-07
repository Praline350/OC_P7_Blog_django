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
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView)
import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('change_password/', authentication.views.ChangePasswordView.as_view(),
         name='password_change'),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.HomeView.as_view(), name='home'),
    path('profile-photo/upload', authentication.views.UploadProfilePhotoView.as_view(),
         name='upload_profile_photo'),
    path('profile/', authentication.views.ProfilePageView.as_view(), name='profile'),
    path('profile/<str:username>/', authentication.views.UserProfileView.as_view(), name='user_profile'),
    path('blog/ticket_upload/', blog.views.TicketUploadView.as_view(), name='ticket_upload'),
    path('blog/ticket/<int:pk>/edit/', blog.views.TicketEditView.as_view(), name='ticket_edit'),
    path('blog/ticket/<int:pk>/delete', blog.views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('blog/ticket/<int:pk>/review_upload/', blog.views.ReviewUploadView.as_view(), name='review_upload'),
    path('blog/review/<int:pk>/edit/', blog.views.ReviewEditView.as_view(), name='review_edit'),
    path('blog/review/<int:pk>/delete/', blog.views.ReviewDeleteView.as_view(), name='review_delete')



]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

