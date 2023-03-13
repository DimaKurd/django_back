import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, authentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bingo
from .permissions import IsPlayer, IsBingoOwner
from .serializers import *
from .serializers import BingoResponseSerializer


class BingoEdit(APIView, LoginRequiredMixin):
    """
    implements post, delete and get methods for work with one Bingo set
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsPlayer, IsBingoOwner]

    @swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: BingoResponseSerializer,
                                    status.HTTP_200_OK: BingoResponseSerializer}
                         )
    def get(self, request: Request, bingo_id: int):
        """
        method for getting words from bingo
        :return:
        """
        try:
            bingo = Bingo.objects.get(bingo_id=bingo_id)
            return Response(data={'id': bingo.bingo_id, 'name': bingo.name, 'words': bingo.words},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'Status': f'Error occurred {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BingoEditSerializer,
                         responses={status.HTTP_400_BAD_REQUEST: BingoResponseSerializer,
                                    status.HTTP_200_OK: BingoResponseSerializer}
                         )
    def post(self, request: Request, bingo_id: int):
        """
        method for editing words and name of bingo
        :param request:
        :param bingo_id:
        :return:
        """
        serializer = BingoEditSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = request.data['name']
        words = request.data['words']
        try:
            if isinstance(words, list) and words and name:
                bingo = Bingo.objects.get(bingo_id=bingo_id)
                bingo.name = name
                bingo.words = words
                bingo.save()
                return Response(data={'Status': 'Bingo was updated'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'Status': 'Smth bad with input data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'Status': f'Error occurred: {e}'})

    @swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: BingoResponseSerializer,
                                    status.HTTP_204_NO_CONTENT: BingoResponseSerializer}
                         )
    def delete(self, request: Request, bingo_id: int):
        """
        method for deleting bingos
        :param request:
        :param bingo_id:
        :return:
        """
        serializer = BingoEditSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            bingo = Bingo.objects.get(bingo_id=bingo_id)
            bingo.delete()
            return Response(data={'Status': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'Status': f'Error occurred: {e}'})


class BingoCommon(LoginRequiredMixin, APIView):
    """
    implement creation and all ids of bingo return
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsPlayer]

    @swagger_auto_schema(request_body=BingoCreateSerializer,
                         responses={status.HTTP_400_BAD_REQUEST: BingoResponseSerializer,
                                    status.HTTP_200_OK: BingoResponseSerializer}
                         )
    def post(self, request: Request):
        """
        Creation of new Bingo
        """
        serializer = BingoCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = request.data['name']
        words = request.data['words']
        try:
            if isinstance(words, list) and words:
                bingo = Bingo.objects.create(author_id=request.user, name=name, words=words)
            else:
                return Response(data={'Status': 'Smth bad with words'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'Status': f'Error occurred: {e}'})

        return Response(data={'Status': f'new bingo created with name {bingo.name}'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: BingoResponseSerializer,
                                    status.HTTP_200_OK: BingoResponseSerializer}
                         )
    def get(self, request: Request):
        """
        Get all bingo ids of authorized player
        :param request:
        :return:
        """
        data = {bingo.bingo_id: bingo.name for bingo in Bingo.objects.filter(author_id=request.user.user_id)}
        return Response(data=data, status=status.HTTP_200_OK)

