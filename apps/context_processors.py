# -*- encoding: utf-8 -*-

from django.conf import settings


def cfg_assets_root(request):
    return {
        'ASSETS_ROOT': settings.ASSETS_ROOT,
        'APP_NAME': settings.APP_NAME
    }
