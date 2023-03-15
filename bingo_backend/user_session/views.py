from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_session.models import UserSession
from user_session.serializers import UserSessionDataSerializer, UserSessionEndpointResponse, \
    UserSessionUpdateProgressSerializer, UserSessionsDataSerializer


class SessionHandler(APIView):
    """
    Class for work with one active user sessions in games
    """

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSessionDataSerializer,
                                    status.HTTP_400_BAD_REQUEST: UserSessionEndpointResponse})
    def get(self, request: Request, game_id):
        """
        Method for user_session providing to client
        :param request:
        :param game_id:
        :return:
        """
        try:
            if request.user.is_authenticated:
                user_session = UserSession.objects.get(player=request.user, game_id=game_id)
                return Response(status=status.HTTP_200_OK, data={'game_id': user_session.game.game_id,
                                                                 'player_id': user_session.player.user_id,
                                                                 'progress': user_session.progress,
                                                                 'random_seed': user_session.random_seed})
            else:
                pass

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something went wrong: {e}'})

    @swagger_auto_schema(request_body=UserSessionUpdateProgressSerializer,
                         responses={status.HTTP_200_OK: UserSessionDataSerializer,
                                    status.HTTP_400_BAD_REQUEST: UserSessionEndpointResponse,
                                    status.HTTP_202_ACCEPTED: UserSessionEndpointResponse})
    def post(self, request: Request, game_id):
        """
        Method for updating progress of UserSession
        :param request:
        :param game_id:
        :return:
        """
        try:
            if request.user.is_authenticated:
                user_session = UserSession.objects.get(player=request.user, game_id=game_id)
                user_session.progress = request.data['progress']
                user_session.save()
                return Response(status=status.HTTP_200_OK, data={'game_id': user_session.game.game_id,
                                                                 'player_id': user_session.player.user_id,
                                                                 'progress': user_session.progress,
                                                                 'random_seed': user_session.random_seed})
            else:
                return Response(status=status.HTTP_202_ACCEPTED, data={'Status': "Not saved 'cause you are guest"})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something went wrong: {e}'})


@api_view(http_method_names=['GET'])
@login_required
@swagger_auto_schema(responses={status.HTTP_200_OK: UserSessionsDataSerializer})
def get_user_sessions(request: Request):
    """
    Method returning all user's sessions
    :param request:
    :return:
    """
    user_sessions = UserSession.objects.filter(player=request.user)
    return Response(status=status.HTTP_200_OK, data=[{'game_id': user_session.game.game_id,
                                                      'player_id': user_session.player.user_id,
                                                      'progress': user_session.progress,
                                                      'random_seed': user_session.random_seed}
                                                     for user_session in user_sessions])