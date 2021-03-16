# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cash = models.IntegerField(default=0)
    contact = models.CharField(max_length=20, blank=True)



class Times(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    times = models.TextField(default="[]")
    sum = models.TimeField(default="00:00:00")
    desc = models.TextField(default="",null=True, blank=True)
    class Meta:
        permissions = (
            ("can_settime", "Can Set Time"),
            ("can_seetimes", "Can See All Times Of Users")
        )

    def __str__(self):
        return self.owner.username

