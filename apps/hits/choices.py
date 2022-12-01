# -*- encoding: utf-8 -*-

"""Choices to Hit App"""
from django.db.models import IntegerChoices


class HitmenStatusChoices(IntegerChoices):
    """Status of Hit """
    ACTIVE = 1
    INACTIVE = 0


class HitStatusChoices(IntegerChoices):
    """Status of Hit """
    ASSIGNED = 0
    FAILED = 1
    COMPLETED = 2
