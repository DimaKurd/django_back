# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bingo.models import Bingo
from game.models import GameSession
from user_session.models import UserSession
from user_session.serializers import UserSessionDataSerializer, UserSessionEndpointResponse, \
    UserSessionUpdateProgressSerializer, UserSessionsDataSerializer


def get_words_by_game_id(game_id: int):
    """
    Accessing to words from bingo
    :param game_id:
    :return:
    """
    game_session = GameSession.objects.filter(game_id=game_id)[0]
    bingo = Bingo.objects.filter(bingo_id=game_session.bingo_id.bingo_id)[0]
    words_bingo = [word.replace('\'', '') for word in bingo.words[1:-1].split('\', ')]

    return words_bingo


class SessionHandler(APIView):
    """
    Class for work with one active user sessions in games
    """

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSessionDataSerializer,
                                    status.HTTP_400_BAD_REQUEST: UserSessionEndpointResponse})
    def get(self, request: Request, session_id):
        """
        Method for user_session providing to client
        :param request:
        :param session_id:
        :return:
        """
        try:
            if request.user.is_authenticated:
                user_session = UserSession.objects.get(session_id=session_id, player=request.user)
                return Response(status=status.HTTP_200_OK, data={'session_id': user_session.session_id,
                                                                 'game_id': user_session.game.game_id,
                                                                 'player_id': user_session.player.id,
                                                                 'progress': user_session.progress,
                                                                 'random_seed': user_session.random_seed,
                                                                 'words': get_words_by_game_id(user_session.game.game_id)})
            else:
                return Response(status=status.HTTP_200_OK, data={'session_id': session_id,
                                                                 'game_id': request.session['game_id'],
                                                                 'player_id': request.session['player_id'],
                                                                 'progress': request.session['progress'],
                                                                 'random_seed': request.session['random_seed'],
                                                                 'words': get_words_by_game_id(request.session['game_id'])})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something went wrong: {e}'})

    @swagger_auto_schema(request_body=UserSessionUpdateProgressSerializer,
                         responses={status.HTTP_200_OK: UserSessionDataSerializer,
                                    status.HTTP_400_BAD_REQUEST: UserSessionEndpointResponse,
                                    status.HTTP_202_ACCEPTED: UserSessionEndpointResponse})
    def post(self, request: Request, session_id):
        """
        Method for updating progress of UserSession
        :param request:
        :param session_id:
        :return:
        """
        try:
            if request.user.is_authenticated:
                user_session = UserSession.objects.get(session_id=session_id, player=request.user)
                user_session.progress = request.data['progress']
                user_session.save()
                return Response(status=status.HTTP_200_OK, data={'session_id': user_session.session_id,
                                                                 'game_id': user_session.game.game_id,
                                                                 'player_id': user_session.player.id,
                                                                 'progress': user_session.progress,
                                                                 'random_seed': user_session.random_seed})
            else:
                return Response(status=status.HTTP_202_ACCEPTED, data={'Status': "Not saved 'cause you are guest"})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something went wrong: {e}'})


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={status.HTTP_200_OK: UserSessionsDataSerializer})
def get_user_sessions(request: Request):
    """
    Method returning all user's sessions
    :param request:
    :return:
    """
    user_sessions = UserSession.objects.filter(player=request.user)
    return Response(status=status.HTTP_200_OK, data=[{'session_id': user_session.session_id,
                                                      'game_id': user_session.game.game_id,
                                                      'player_id': user_session.player.id,
                                                      'progress': user_session.progress,
                                                      'random_seed': user_session.random_seed}
                                                     for user_session in user_sessions])


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={status.HTTP_204_NO_CONTENT: UserSessionEndpointResponse,
                                status.HTTP_400_BAD_REQUEST: UserSessionEndpointResponse})
def exit_game(request: Request, session_id: int):
    """
        Method for exiting from user_session, i.e. exit from the game
        :param request:
        :param session_id:
        :return:
        """

    try:
        UserSession.objects.get(session_id=session_id, player=request.user).delete()
        return Response(status=status.HTTP_200_OK, data={'Status': 'Exit successful'})
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'Status': f'Something went wrong: {e}'})
