
from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from inventories.models import Inventory


# Create your models here.



def get_absolute_url(self):
    return reverse("accounts:account", kwargs={"pk": self.pk})
User.add_to_class('get_absolute_url', get_absolute_url)

def get_update_url(self):
    return reverse("accounts:edit", kwargs={"pk": self.pk})
User.add_to_class('get_update_url', get_update_url)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.DecimalField(max_digits=12, decimal_places=0, blank=True ,null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        Inventory.objects.create(client=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_groups(sender, instance, **kwargs):

    if instance.groups.filter(name='banned').exists():
        # data panel:
        # instance tried connect banned account
        return

    elif instance:
        group, ok = Group.objects.get_or_create(name="default")
        group.user_set.add(instance)

