from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Role(models.Model):
    role_id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(unique=True, null=False, max_length=40)


class User(AbstractUser):
    user_id = models.IntegerField(primary_key=True, auto_created=True)
    nickname = models.CharField(max_length=40, unique=True, null=False)
    role = models.ManyToManyField(to=Role, related_name='role')

    def is_player(self):
        return self.role == Role.objects.get(name='player')


