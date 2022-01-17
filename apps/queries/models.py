import uuid
import os
from django.db import models

from config.utils import generate_unique_slug


def get_private_key(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('pkeys', filename)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=1000)
    slug = models.SlugField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.name) > 0:
                self.slug = generate_unique_slug(self)
        super(Category, self).save(*args, **kwargs)


class Database(models.Model):
    types = (
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL')
    )
    methods = (
        ('password', 'Password'),
        ('private_key', 'Private key')
    )
    type = models.CharField(max_length=255, default='postgresql', choices=types)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    db_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    use_ssh = models.BooleanField(default=False)
    ssh_host = models.CharField(max_length=255, blank=True, null=True)
    ssh_port = models.IntegerField(blank=True, null=True)
    ssh_user_name = models.CharField(max_length=255, blank=True, null=True)
    ssh_method = models.CharField(max_length=255, default='password', choices=methods)
    ssh_password = models.CharField(max_length=255, blank=True, null=True)
    ssh_private_key = models.FileField(upload_to=get_private_key, blank=True, null=True)

    def __str__(self):
        return self.name


class Query(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=1000)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    query = models.TextField(null=True, blank=True)
    order_by = models.CharField(max_length=255, null=True)
    pagination = models.BooleanField(default=True)
    page_size = models.IntegerField(default=50)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="queries")
    database = models.ForeignKey(
        Database,
        on_delete=models.DO_NOTHING,
        related_name="queries")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.title) > 0:
                self.slug = generate_unique_slug(self, property='title')
        super(Query, self).save(*args, **kwargs)


class Param(models.Model):
    types = (
        ('int', 'Integer'),
        ('float', 'Float'),
        ('text', 'Text'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='text', choices=types)
    default = models.CharField(max_length=255, null=True, blank=True)
    query = models.ForeignKey(
        Query,
        on_delete=models.DO_NOTHING,
        related_name="params")

    def __str__(self):
        return self.name
