from django.urls import path

from . import views

urlpatterns = [
    path('<int:bingo_id>', views.BingoEdit.as_view()),
    path('', views.BingoCommon.as_view())
]