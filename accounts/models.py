
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save

from inventories.models import Inventory
from orders.models import Order

# Create your models here.



def get_account_url(self):
    return reverse("accounts:account", kwargs={"pk": self.pk})
User.add_to_class('get_account_url', get_account_url)

def get_edit_account_url(self):
    return reverse("accounts:edit", kwargs={"pk": self.pk})
User.add_to_class('get_edit_account_url', get_edit_account_url)

# class Abstract(AbstractUser):
#     pass

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

