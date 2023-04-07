from django.contrib.auth.models import AbstractUser
from django.db import models


# class Role(models.Model):
#     role_id = models.IntegerField(primary_key=True, auto_created=True)
#     name = models.CharField(unique=True, null=False, max_length=40)


class User(AbstractUser):
    id = models.IntegerField(primary_key=True, auto_created=True)
    nickname = models.CharField(max_length=40, unique=True, null=False)
    # role = models.ManyToManyField(to=Role, related_name='role')



