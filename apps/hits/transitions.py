# -*- encoding: utf-8 -*-

from django_fsm import transition
from apps.hits.choices import HitmenStatusChoices, HitStatusChoices
from apps.hits.utils import check_boss_to_inactive_user, check_can_modify_state_hit
from core.settings import BIG_BOSS_ID


class HitmenTransitions:
    @transition(
        field="state",
        source=HitmenStatusChoices.ACTIVE,
        target=HitmenStatusChoices.INACTIVE,
        conditions=[check_boss_to_inactive_user],
        custom=dict(verbose="Disable user"),
    )
    def set_inactive_user(self, **kwargs):
        user = self.user
        if not user.id == BIG_BOSS_ID:
            user.is_active = False
            user.save()
        else:
            return 'Action not legal. You are a BIG BOSS'


class HitTransitions:
    @transition(
        field="state",
        source=HitStatusChoices.ASSIGNED,
        target=HitStatusChoices.COMPLETED,
        conditions=[check_can_modify_state_hit],
        custom=dict(verbose="Mission Completed"),
    )
    def set_completed_hit(self, **kwargs):
        pass

    @transition(
        field="state",
        source=HitStatusChoices.ASSIGNED,
        target=HitStatusChoices.FAILED,
        conditions=[check_can_modify_state_hit],
        custom=dict(verbose="Mission Failed"),
    )
    def set_failed_hit(self, **kwargs):
        pass
