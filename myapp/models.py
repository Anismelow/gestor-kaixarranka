from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta,time




# Create your models here.

class Horas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    horas_laboradas = models.DurationField(null=True, editable=False)

    def calcular_horas_trabajadas(self) -> timedelta:
        """
        Calcula las horas trabajadas considerando la posibilidad de cruce de medianoche.
        """
        entrada = datetime.combine(self.fecha, self.hora_entrada)
        salida = datetime.combine(self.fecha, self.hora_salida)
        
        # Ajustar la hora de salida si es antes de la hora de entrada (cruce de medianoche)
        if salida < entrada:
            salida += timedelta(days=1)  # Añadir un día a la hora de salida
        
        return salida - entrada

    def save(self, *args, **kwargs):
        # Calcular las horas trabajadas usando el método
        self.horas_laboradas = self.calcular_horas_trabajadas()
        super().save(*args, **kwargs)
        
class Adelanto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha_solicitud} - {self.monto}"
