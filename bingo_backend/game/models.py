from django.db import models

# Create your models here.
from bingo.models import Bingo


class GameSession(models.Model):
    game_id = models.IntegerField(primary_key=True)
    bingo_id = models.ForeignKey(to=Bingo, to_field='bingo_id', on_delete=models.CASCADE)
    launched = models.BooleanField(default=False, null=False)
    join_code = models.TextField(null=False, unique=True, default='1q2w3e4r')
