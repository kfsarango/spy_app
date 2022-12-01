# -*- encoding: utf-8 -*-
from core.settings import BIG_BOSS_ID


def get_user_tracing():
    from tracing.middleware import TracingMiddleware
    info = TracingMiddleware.get_info()
    return info.get('user', False)


def check_boss_to_inactive_user(instance):
    user = get_user_tracing()
    return user.id == BIG_BOSS_ID


def check_can_modify_state_hit(instance):
    user = get_user_tracing()

    is_owner = user.id == instance.assigned_to.id
    is_valid_boss = instance.assigned_to.id in user.hitmen.get_all_lackeys_ids()

    return is_owner or is_valid_boss
