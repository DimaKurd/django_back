import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

# Create your views here.
from .models import User, Role


@require_http_methods(["POST"])
def register(request: HttpRequest):
    try:
        users = User.objects.filter(nickname=request.POST['nickname'])
        if users:
            return HttpResponse(status=400, content=json.dumps('User already exists with such nickname'))
        else:
            user = User.objects.create_user(nickname=request.POST['nickname'], password=request.POST['password'],
                                            username=request.POST['nickname'])
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps(f'{e}'))

    user = User.objects.get(nickname=user.nickname)
    user.role.set([Role.objects.get(name='player')])
    user.save()

    return HttpResponse(content=json.dumps({'status': 'Success'}), status=200)


@require_http_methods(["POST"])
def login_to_bingo(request: HttpRequest):
    nickname = request.POST['nickname']
    password = request.POST['password']
    user = authenticate(username=nickname, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(status=200, content=json.dumps({'status': 'Successful'}))
    else:
        return HttpResponse(status=403, content=json.dumps({'status': 'Fault'}))


@require_http_methods(["POST"])
def easy_login_to_bingo(request: HttpRequest):
    nickname = request.POST['nickname']
    try:
        temp_user = User.objects.create_user(nickname=request.POST['nickname'], password='1234',
                                             username=request.POST['nickname'])
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps(f'{e}'))

    temp_user = User.objects.get(nickname=temp_user.nickname)
    temp_user.role.add(Role.objects.get(name='ghost'))
    user = authenticate(username=nickname, password='1234')
    if user is not None:
        login(request, user)
        return HttpResponse(status=200, content=json.dumps({'status': 'Successful'}))
    else:
        return HttpResponse(status=403, content=json.dumps({'status': 'Fault'}))


@require_http_methods(["GET"])
def logout_bingo(request):
    logout(request)
    return HttpResponse(status=200, content=json.dumps({'status': 'Logout successful'}))


@ensure_csrf_cookie
@login_required
def index(request):
    return HttpResponse(f"Hello {request.user.username}")
