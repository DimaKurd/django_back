from rest_framework import permissions

from bingo.models import Bingo
from game.models import GameSession


class IsGameSessionOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to get info and edir game_session
    """
    def has_permission(self, request, view):
        try:
            game_session = GameSession.objects.get(game_id=view.kwargs['game_id'])
        except:
            return False

        try:
            status = Bingo.objects.get(bingo_id=game_session.bingo_id.bingo_id).author_id == request.user
        except:
            return False
        return status