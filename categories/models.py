
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import slugify_instance
# Create your models here.

class Category(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    active = models.BooleanField(default=True)

    def directory_path(instance, filename):
        return f"categories/category_{instance.id}/{filename}"

    def default_directory_path():
        return "categories/default/categories-default-icon.jpg"
    image = models.ImageField(upload_to= directory_path, default=default_directory_path, blank=True, null=True)


    def __str__(self) -> str:
        return self.name

    # reverse urls

    def get_category_url(self):
        return reverse("categories:category", kwargs={"name": self.name})

    def get_update_url(self):
        return reverse("categories:update", kwargs={"name": self.name})

    def get_delete_url(self):
        return reverse("categories:delete", kwargs={"name": self.name})



def category_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance, save=False)
pre_save.connect(category_pre_save, sender=Category)

def category_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance(instance, save=True)
post_save.connect(category_post_save, sender=Category)