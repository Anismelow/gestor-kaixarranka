from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


# Register your models here.

@admin.register(Horas)
class HorasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora_entrada','hora_salida', 'horas_laboradas')
    list_filter = ('usuario', 'fecha')
    search_fields = ('usuario','fecha')



@admin.register(Adelanto)
class AdelantoAdmin(admin.ModelAdmin):
    list_display = ('usuario','fecha_solicitud','monto')
    list_filter = ('usuario','fecha_solicitud')
    search_fields = ('usuario','fecha')



user = User.objects.get(username='beatriz' or 'admin')
print(user.is_staff)  # Debería imprimir True
