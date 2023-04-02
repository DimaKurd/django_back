from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.get_user_sessions),
    path('<int:session_id>', SessionHandler.as_view()),
    path('<int:session_id>/exit', exit_game)
]
