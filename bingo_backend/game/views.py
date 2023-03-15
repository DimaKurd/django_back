import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bingo.models import Bingo
from game.models import GameSession
from game.permissions import IsGameSessionOwner
from game.serializers import (GameEndpointResponseSerializer, SingleGameDataResponse, GameCreationDataSerializer,
                              ManyGameDataResponse, GameConnectDataSerializer)
from user_session.models import UserSession
from user_session.serializers import UserSessionDataSerializer


class GameManage(LoginRequiredMixin, APIView):
    """
    implements connection to game, getting game info update game settings and removing game from DB
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsGameSessionOwner]

    @swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer,
                                    status.HTTP_200_OK: SingleGameDataResponse})
    def get(self, request, game_id):
        """
        method for providing info about game
        :param game_id:
        :return:
        """
        try:
            game_session = GameSession.objects.get(game_id=game_id)
            data = {'game_id': game_session.game_id, 'bingo_id': game_session.bingo_id.bingo_id,
                    'launched': game_session.launched, 'max_players': game_session.max_players}
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'Status': f'Something went wrong: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=GameCreationDataSerializer,
                         responses={status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer,
                                    status.HTTP_403_FORBIDDEN: GameEndpointResponseSerializer,
                                    status.HTTP_200_OK: SingleGameDataResponse})
    def put(self, request, game_id):
        """
        method for updating game_session object
        :param request:
        :param game_id:
        :return:
        """
        serializer = GameCreationDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            bingo = Bingo.objects.get(bingo_id=request.data['bingo_id'])
            if request.user == bingo.author_id:
                game_session = GameSession.objects.get(game_id=game_id)
                game_session.max_players = request.data.get('max_players')
                game_session.bingo_id = bingo
                game_session.save()
                data = {'game_id': game_session.game_id, 'bingo_id': game_session.bingo_id.bingo_id,
                        'launched': game_session.launched, 'max_players': game_session.max_players}
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN, data={'Status': f'Not yours bingo. Ha-ha'})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something wrong: {e}'})

    @swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer,
                                    status.HTTP_204_NO_CONTENT: GameEndpointResponseSerializer}
                         )
    def delete(self, request: Request, game_id: int):
        """
        method for deleting game_sessions
        :param request:
        :param game_id:
        :return:
        """
        try:
            game_session = GameSession.objects.get(game_id=game_id)
            game_session.delete()
            return Response(data={'Status': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'Status': f'Error occurred: {e}'})


class GameCommon(LoginRequiredMixin, APIView):
    """
    Implements creation and provide info about user games
    """
    authentication_classes = [authentication.SessionAuthentication]

    @swagger_auto_schema(responses={status.HTTP_200_OK: ManyGameDataResponse})
    def get(self, request):
        """
        Method for providing info about all player's games
        :param request:
        :return:
        """
        game_sessions = GameSession.objects.filter(bingo_id__author_id=request.user)
        data = [{'game_id': game_session.game_id, 'bingo_id': game_session.bingo_id.bingo_id,
                 'launched': game_session.launched, 'max_players': game_session.max_players} for game_session in
                game_sessions]
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=GameCreationDataSerializer,
                         responses={status.HTTP_403_FORBIDDEN: GameEndpointResponseSerializer,
                                    status.HTTP_200_OK: GameEndpointResponseSerializer,
                                    status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer}
                         )
    def post(self, request):
        """
        Method for creating new game
        :param request:
        :return:
        """
        serializer = GameCreationDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            bingo = Bingo.objects.get(bingo_id=request.data['bingo_id'])
            if request.user == bingo.author_id:
                game_session = GameSession.objects.create(bingo_id=bingo, launched=False,
                                                          max_players=request.data.get('max_players'))
                # TODO Remove this Costyl
                game_session = GameSession.objects.filter(bingo_id=game_session.bingo_id).order_by('-game_id')[0]
                return Response(status=status.HTTP_201_CREATED, data={'Status': f'New gameSession created with '
                                                                                f'id {game_session.game_id}'})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN, data={'Status': f'Not yours bingo. Ha-ha'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something wrong: {e}'})


@api_view(http_method_names=['POST'])
@permission_classes([IsGameSessionOwner])
@login_required
@swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer,
                                status.HTTP_200_OK: GameEndpointResponseSerializer})
def start_game(request, game_id):
    """
    Method for starting game
    :param request:
    :param game_id:
    :return:
    """
    try:
        game_session = GameSession.objects.get(game_id=game_id)
        game_session.launched = True
        game_session.save()
        return Response(data={'Status': 'Game started!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'Status': f'Something went wrong {e}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes([IsGameSessionOwner])
@login_required
@swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer,
                                status.HTTP_200_OK: GameEndpointResponseSerializer})
def stop_game(request, game_id):
    """
    Method for stopping game
    :param request:
    :param game_id:
    :return:
    """
    try:
        game_session = GameSession.objects.get(game_id=game_id)
        game_session.launched = False
        game_session.save()
        return Response(data={'Status': 'Game stopped!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'Status': f'Something went wrong {e}'}, status=status.HTTP_400_BAD_REQUEST)


class Connection(APIView):
    @swagger_auto_schema(request_body=GameConnectDataSerializer,
                         responses={status.HTTP_200_OK: UserSessionDataSerializer,
                                    status.HTTP_406_NOT_ACCEPTABLE: GameEndpointResponseSerializer,
                                    status.HTTP_400_BAD_REQUEST: GameEndpointResponseSerializer
                                    })
    def post(self, request: Request):
        """
        Method for connection to game for authenticated or guest user
        :param request:
        :return:
        """

        serializer = GameConnectDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            game = GameSession.objects.get(game_id=request.data['game_id'])
            if request.user.is_authenticated:
                if game.launched:
                    user_session, _ = UserSession.objects.get_or_create(player=request.user, game=game)
                    return Response(status=status.HTTP_200_OK, data={'game_id': user_session.game.game_id,
                                                                     'player_id': user_session.player.user_id,
                                                                     'progress': user_session.progress,
                                                                     'random_seed': user_session.random_seed})
                else:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'Status': 'Game not started'})
            else:
                pass

        except Exception as e:
            return Response(data={'Status': f'Something went wrong {e}'}, status=status.HTTP_400_BAD_REQUEST)
