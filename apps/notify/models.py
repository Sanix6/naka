from django.db import models
from apps.users.models import User

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Если пусто — отправится всем пользователям"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"Уведомление для {self.user.email} - {self.title}"
        return f"Уведомление для всех - {self.title}"
