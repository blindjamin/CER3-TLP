from django.db import models
from django.conf import settings

class Notificacion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username}: {'Leída' if self.leida else 'No leída'}"
