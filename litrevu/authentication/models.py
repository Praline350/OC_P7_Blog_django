from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    profile_photo = models.ImageField(
        verbose_name="Profile photo", upload_to="profile_photos/", null=True, blank=True
    )

    IMAGE_MAX_SIZE = (400, 400)

    def resize_profile_photo(self):
        profile_photo = Image.open(self.profile_photo)
        profile_photo.thumbnail(self.IMAGE_MAX_SIZE)
        profile_photo.save(self.profile_photo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (
            self.profile_photo
        ):  # Vérifiez si une photo de profil existe avant de redimensionner
            self.resize_profile_photo()
