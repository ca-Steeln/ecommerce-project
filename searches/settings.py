
from categories.models import Category
from products.models import Product

# Create your views here.

SEARCH_TYPE_MAPPING = {

    'categories': Category,
    'products': Product
}