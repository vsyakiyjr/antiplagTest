from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from reports.models import Report
from django.contrib.auth.models import User


class Stats(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reports_count = models.IntegerField()
    symbols_used = models.IntegerField()
    symbols_left = models.IntegerField()

    # def copy(self):
    #     new_obj = self.__class__()
    #     for field in self._meta.fields:
    #         setattr(new_obj, field.name, getattr(self, field.name))
    #     return new_obj


def create_user_stats(sender, instance, created, **kwargs):
    if created:
        stats = Stats(user=instance)
        stats.reports_count = 0
        stats.symbols_used = 0
        stats.symbols_left = 1000000
        stats.save()

def add_report(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        last_stats = Stats.objects.filter(user=user).last()
        reports_count = last_stats.reports_count
        symbols_used = last_stats.symbols_used
        symbols_left = last_stats.symbols_left
        reports_count += 1
        Stats.objects.create(user=user, reports_count=reports_count, symbols_used=symbols_used, symbols_left=symbols_left)

post_save.connect(create_user_stats, sender=User)
post_save.connect(add_report, sender=Report)
