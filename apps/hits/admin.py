# -*- encoding: utf-8 -*-

from django.contrib import admin

from apps.hits.models import Hitmen


# Register your models here
class HitmenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hitmen, HitmenAdmin)
