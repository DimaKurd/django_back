from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_to_bingo, name='login'),
    path('easy_login', views.easy_login_to_bingo, name='easy_login'),
    path('logout', views.logout_bingo, name='logout')
]
