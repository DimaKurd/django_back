import random

from django.db import models

# Create your models here.
from game.models import GameSession
from user.models import User


class UserSession(models.Model):
    session_id = models.IntegerField(primary_key=True)
    game = models.ForeignKey(to=GameSession, to_field='game_id', on_delete=models.CASCADE)
    player = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE)
    progress = models.TextField(null=True)
    random_seed = models.IntegerField(null=False, default=42)

