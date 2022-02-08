from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.queries.models import Query


class User(AbstractUser):
    queries = models.ManyToManyField(Query, "queries", null=True, blank=True)

    def __str__(self):
        return self.username
