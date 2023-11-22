
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q

from registration.models import CustomUser
from categories.models import Category

from .utils import slugify_instance

# Create your models here.

class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None:
            return self.none()

        lookups = Q(title__icontains=query) | Q(name__icontains=query)
        return self.filter(lookups)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, editable=False) # need a test
    name = models.CharField(max_length=128, default='Product', null=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=5000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(blank=True, null=True)
    has_discount = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    objects = ProductManager()

    def directory_path(instance, filename):
        return f"products/product_{instance.id}/{filename}"

    def default_directory_path():
        return "products/defaults/default-icon.jpg"
    image = models.ImageField(upload_to= directory_path, default=default_directory_path, blank=True, null=True)


    def __str__(self) -> str:
        return self.title

    # reverse urls

    def get_absolute_url(self):
        return reverse("products:product", kwargs={"slug": self.slug})

    def get_add_url(self):
        return reverse("products:add", kwargs={"slug": self.slug})

    def get_order_url(self):
        return reverse("products:order", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("administration:product-delete", kwargs={"slug": self.slug})

    def get_manage_url(self):
        return reverse("administration:product", kwargs={"slug": self.slug})

def product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance, save=False)
pre_save.connect(product_pre_save, sender=Product)

def product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance(instance, save=True)
post_save.connect(product_post_save, sender=Product)


class ProductItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.product.name