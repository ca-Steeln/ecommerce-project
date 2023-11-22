
from django.db import models
from django.urls import reverse
from django.db.models import Q

from registration.models import CustomUser

# Create your models here.

class SearchesQuertSet(models.QuerySet):
    def search(self, query=None):
        if query is None:
            return self.none()

        lookups = Q(title__icontains=query) | Q(name__icontains=query)
        return self.filter(lookups)

class SearchesManager(models.Manager):

    def get_queryset(self):
        return SearchesQuertSet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

class Search(models.Model):

    objects = SearchesManager()
