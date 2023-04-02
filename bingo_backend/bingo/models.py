from django.db import models

from user.models import User


class Bingo(models.Model):
    bingo_id = models.IntegerField(primary_key=True, auto_created=True)
    author_id = models.ForeignKey(to=User, to_field='user_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    words = models.TextField(null=False)
