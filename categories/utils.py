

from string import ascii_lowercase, ascii_uppercase
from random import shuffle, randint
from uuid import uuid4

def create_uu_slug(min_char:int = 3, max_char:int = 5) -> str:
    s1 = list(ascii_lowercase)
    s2 = list(ascii_uppercase)
    s4 = list(str(uuid4()).split('-'))

    characters_number = randint(min_char, max_char)

    shuffle(s1)
    shuffle(s2)

    slug = []

    for i in range(round(characters_number * (60/100))):
        slug.append(s1[i])
        slug.append(s2[i])


    for i in range(round(characters_number * (40/100))):
        slug.append(s4[i])

    shuffle(slug)
    slug = "".join(slug)
    return slug


def slugify_instance(instance, save=False, new_slug=None):
    slug = create_uu_slug()
    klass = instance.__class__
    qs = klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        if qs.exists():
            slug = create_uu_slug(min_char=4, max_char=6)
            return slugify_instance(instance, save, slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance