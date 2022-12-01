# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_fsm import FSMIntegerField
from apps.hits.choices import HitmenStatusChoices, HitStatusChoices
from apps.hits.transitions import HitmenTransitions, HitTransitions


# Create your models here.
class Hitmen(models.Model, HitmenTransitions):
    description = models.TextField(null=True, blank=True)
    is_boss = models.BooleanField(default=False)
    state = FSMIntegerField(default=HitmenStatusChoices.ACTIVE, choices=HitmenStatusChoices.choices, protected=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='hitmen')

    @property
    def get_group_names(self):
        """Names group of Hitmen"""
        groups = Group.objects.filter(hitmens=self.id)
        if groups:
            return ' - '.join([group.name for group in groups])

        return '-'

    def get_all_lackeys_ids(self):
        """Only ID of Hitmens members of Groups"""
        if self.is_boss:
            groups = self.groups.all()
            lackeys = []
            for group in groups:
                lackeys.extend(group.hitmens.all())
            return [lackey.id for lackey in lackeys]

        return []

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = "Hitmen"
        verbose_name_plural = "Hitmens"


class Group(models.Model):
    name = models.CharField(max_length=128)
    boss = models.ForeignKey(Hitmen, on_delete=models.PROTECT, related_name='groups')
    hitmens = models.ManyToManyField(Hitmen)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Hit(models.Model, HitTransitions):
    target_name = models.CharField(max_length=128)
    description = models.TextField()
    assigned_by = models.CharField(max_length=128)
    state = FSMIntegerField(default=HitStatusChoices.ASSIGNED, choices=HitStatusChoices.choices, protected=True)
    created_date = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(Hitmen, on_delete=models.PROTECT, related_name='hits')

    def __str__(self):
        return f'Case: {self.target_name}'

    class Meta:
        verbose_name = "Hit"
        verbose_name_plural = "Hits"
