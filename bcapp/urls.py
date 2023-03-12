from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.dishome,name='dishome'),
path('register', views.dis1,name='dis1'),
    path('vote',views.votecand,name="votecand"),
    path('result',views.disresult,name="disresult"),
    path('reg_user',views.reg_user,name="reg_user"),
    path('change_state',views.change_state,name="change_state")
]