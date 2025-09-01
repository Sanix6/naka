from django.contrib import admin
from .models import Notification
from .services import send_onesignal_notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "sent", "created_at")
    actions = ["send_notifications"]

    def send_notifications(self, request, queryset):
        for notif in queryset:
            if notif.sent:
                continue
            send_onesignal_notification(
                title=notif.title,
                message=notif.message,
                user=notif.user
            )
            notif.sent = True
            notif.save()
        self.message_user(request, "Выбранные уведомления были отправлены.")

    send_notifications.short_description = "Отправить выбранные уведомления"
