from django.urls import path
from .views import *

urlpatterns = [
    path('login/', inicio_sesion, name='login'),
    path('home/', view_home, name='home'),
    path('horas_detail/',horas_detail , name='horasdetail'),
    path('adelanto_detail/',adelanto_detail , name='adelantodetail'),
    path('logout/', cerrar_sesion, name='logout'),
]
