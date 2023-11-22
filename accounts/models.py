
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


from phonenumber_field.modelfields import PhoneNumberField

from inventories.models import Inventory
from project.settings import USER_STATUS_CHOICES, ACTIVE_USER, USER_ROLES_CHOICES, DEFAULT_ROLE
from registration.models import CustomUser

from .settings import (REGION_CHOICES, DZ)
# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # needs default value or change null system
    phone = PhoneNumberField(max_length=13, blank=True, region=DZ)

    def directory_path(instance, filename):
        return f"accounts/account_{instance.id}/{filename}"
    def default_directory_path():
        return "accounts/defaults/default-icon.jpg"
    image = models.ImageField(upload_to= directory_path, default=default_directory_path, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:account", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("accounts:edit", kwargs={"pk": self.pk})

    def get_manage_url(self):
        return reverse("administration:account", kwargs={"pk": self.pk})


@receiver(post_save, sender=CustomUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        Inventory.objects.create(client=instance)


