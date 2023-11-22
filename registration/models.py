

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.http import Http404, HttpResponseForbidden
from django.db.models import Q
from django.utils import timezone


from project.settings import (
    USER_STATUS_CHOICES, USER_ROLES_CHOICES,
    ACTIVE_USER, BANNED_USER, DELETED_USER,
    DEFAULT_ROLE, ADMIN_ROLE, MOD_ROLE, MANAGER_ROLE,
    CLIENT_GROUP,
    )
# Create your models here.


class CustomUserQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None:
            return self.none()

        lookups = Q(username__icontains=query) | Q(id__icontains=query)
        return self.filter(lookups)

    # STATUS
    def active(self, count=False):
        qs = self.filter(status=ACTIVE_USER)
        return qs.count() if count else qs

    def banned(self, count=False):
        qs = self.filter(status=BANNED_USER)
        return qs.count() if count else qs

    def deleted(self, count=False):
        qs = self.filter(status=DELETED_USER)
        return qs.count() if count else qs

    # ROLE
    def admin(self, count=False):
        qs = self.filter(role=ADMIN_ROLE)
        return qs.count() if count else qs

    def mod(self, count=False):
        qs = self.filter(role=MOD_ROLE)
        return qs.count() if count else qs

    def manager(self, count=False):
        qs = self.filter(role=MANAGER_ROLE)
        return qs.count() if count else qs

    def default(self, count=False):
        qs = self.filter(role=DEFAULT_ROLE)
        return qs.count() if count else qs


class CustomUserManager(UserManager):
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

class CustomUser(AbstractUser):
    is_mod = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=USER_ROLES_CHOICES, default=DEFAULT_ROLE)
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default=ACTIVE_USER)

    objects = CustomUserManager()


    def get_dashboard_url(self):
        return reverse("dashboard:user", kwargs={"pk": self.pk})

    def get_user_orders_url(self):
        return reverse("administration:client-orders", kwargs={"client_pk": self.pk})

    def get_manage_url(self):
        return reverse("administration:user", kwargs={"pk": self.pk})

    def set_banned(self):
        return reverse("administration:set-banned", kwargs={"pk": self.pk})

    def set_default(self):
        return reverse("administration:set-default", kwargs={"pk": self.pk})

    def set_mod(self):
        return reverse("administration:set-mod", kwargs={"pk": self.pk})

    def set_manager(self):
        return reverse("administration:set-manager", kwargs={"pk": self.pk})

@receiver(post_save, sender=CustomUser)
def user_groups(sender, instance, created, **kwargs):

    if created:
        group, created = Group.objects.get_or_create(name=CLIENT_GROUP)
        group.user_set.add(instance)
        return

    elif instance.groups.filter(name='banned').exists():
        # data panel:
        # instance tried connect banned account
        return HttpResponseForbidden()

    elif instance:
        CustomUser.objects.filter(pk=instance.pk).update(last_login=timezone.now())
