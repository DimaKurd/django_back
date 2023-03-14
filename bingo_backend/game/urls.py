from django.urls import path

from . import views

urlpatterns = [
    path('<int:game_id>', views.GameManage.as_view()),
    path('', views.GameCommon.as_view()),
    path('<int:game_id>/start', views.start_game),
    path('<int:game_id>/stop', views.stop_game)
]