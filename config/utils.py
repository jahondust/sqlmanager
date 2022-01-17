import string
import random
from django.utils.text import slugify
from transliterate import translit


def random_str_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_unique_slug(instance, new_slug=None, property='name',):
    if new_slug is None:
        name = translit(getattr(instance, property), 'ru', reversed=True)
        new_slug = slugify(name)

    Klass = instance.__class__
    qs = Klass.objects.filter(slug=new_slug).exists()

    if qs:
        new_slug = "{slug}-{random_str}".format(slug=new_slug, random_str=random_str_generator(size=4))
        return generate_unique_slug(instance, new_slug=new_slug)

    return new_slug
