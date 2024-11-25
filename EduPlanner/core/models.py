from django.db import models

class Notificacion(models.Model):
    event = models.ForeignKey(
        'eventos.Evento',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.event.title}"
