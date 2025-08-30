from django.apps import AppConfig


class WhitebitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.whitebitx'
    verbose_name = 'Криптовалюты'

    def ready(self):
        from django.contrib.admin.sites import site
        from django_otp.plugins.otp_totp.models import TOTPDevice
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        import json
        if TOTPDevice in site._registry:
            site.unregister(TOTPDevice)


        if not PeriodicTask.objects.filter(name="update_rates_task").exists():
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.MINUTES
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name="update_rates_task",
                task="apps.whitebitx.tasks.update_rates_from_ticker",
                enabled=True,
                kwargs=json.dumps({})
            )
