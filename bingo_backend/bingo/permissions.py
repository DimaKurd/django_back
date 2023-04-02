from rest_framework import permissions
from rest_framework.request import Request

from bingo.models import Bingo


# class IsPlayer(permissions.BasePermission):
#     """
#     Custom permission to only allow players to create new bingos
#     """
#
#     def has_permission(self, request: Request, view):
#         #
#         for role in request.user.role.all():
#             if role.name == 'player':
#                 return True
#         return False


class IsBingoOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit their bingos
    """

    def has_permission(self, request, view):
        try:
            bingo = Bingo.objects.get(bingo_id=view.kwargs['bingo_id'])
        except:
            return False
        return bingo.author_id == request.user
