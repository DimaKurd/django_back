import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User, Role
from .serializers import *


@swagger_auto_schema(request_body=UserSerializer, method='post')
@api_view(http_method_names=["POST"])
def register(request: Request):
    """
    Entrypoint for registration of new user as player
    :param request:
    :return:
    """
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        users = User.objects.filter(nickname=request.data['nickname'])
        if users:
            return Response(json.dumps('User already exists with such nickname'), status=400)
        else:
            user = User.objects.create_user(nickname=request.data['nickname'], password=request.data['password'],
                                            username=request.data['nickname'])
    except Exception as e:
        return Response(json.dumps(f'{e}'), status=400, )

    user = User.objects.get(nickname=user.nickname)
    user.role.set([Role.objects.get(name='player')])
    user.save()

    return Response(json.dumps({'status': 'Success'}), status=200)


@swagger_auto_schema(request_body=UserSerializer, method='post')
@api_view(http_method_names=["POST"])
def login_to_bingo(request: Request):
    """
    entrypoint for login to bingo as player
    :param request:
    :return:
    """
    nickname = request.data['nickname']
    password = request.data['password']
    user = authenticate(username=nickname, password=password)
    if user is not None:
        login(request, user)
        return Response(json.dumps({'status': 'Successful'}), status=200)
    else:
        return Response(json.dumps({'status': 'Fault'}), status=403)


@swagger_auto_schema(request_body=GuestSerializer, method='post')
@api_view(["POST"])
def easy_login_to_bingo(request: Request):
    """
    entrypoint for easy registration as guest (ghost)
    :param request:
    :return:
    """
    serializer = GuestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    nickname = request.data['nickname']
    try:
        temp_user = User.objects.create_user(nickname=request.data['nickname'], password='1234',
                                             username=request.data['nickname'])
    except Exception as e:
        return Response(json.dumps(f'{e}'), status=status.HTTP_400_BAD_REQUEST)

    temp_user = User.objects.get(nickname=temp_user.nickname)
    temp_user.role.add(Role.objects.get(name='ghost'))
    user = authenticate(username=nickname, password='1234')
    if user is not None:
        login(request, user)
        return Response(json.dumps({'status': 'Successful'}), status=status.HTTP_200_OK)
    else:
        return Response(json.dumps({'status': 'Fault'}), status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
def logout_bingo(request):
    """
    logout
    :param request:
    :return:
    """
    logout(request)
    return Response(json.dumps({'status': 'Logout successful'}), status=status.HTTP_200_OK)


@ensure_csrf_cookie
@api_view(["GET"])
def index(request):
    """
    entrypoint for assuring that login is successful and csrf is set
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return Response(f"Hello {request.user.username}")
    else:
        return Response('Hello ghost')
