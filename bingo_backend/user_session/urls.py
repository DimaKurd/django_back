from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.get_user_sessions),
    path('<int:game_id>', SessionHandler.as_view())
]
