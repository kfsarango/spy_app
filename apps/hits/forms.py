# -*- encoding: utf-8 -*-

from django import forms
from django.db.models import Q

from apps.hits.models import Hit, Group, Hitmen
from apps.hits.utils import get_user_tracing
from core.settings import BIG_BOSS_ID


class HitForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = (
            'target_name',
            'description',
            'assigned_to'
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"placeholder": "Brief description", "row": 2}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = get_user_tracing()

        hitmen_queryset = Hitmen.objects.filter(user__is_active=True)
        if user.id == BIG_BOSS_ID:
            qs_exclude = Q(**{'user__id': 1})
        else:
            qs_exclude = Q(**{'user__id': 1}) | Q(
                **{'is_boss': True}
            )
            hitmen_queryset = hitmen_queryset.filter(
                id__in=user.hitmen.get_all_lackeys_ids()
            )

        self.fields['assigned_to'].queryset = hitmen_queryset.exclude(qs_exclude)


class HitInactiveAssignedForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = (
            'target_name',
            'description',
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"placeholder": "Brief description", "row": 2}
            ),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if self.instance and instance.pk:
            self.fields['boss'].initial = instance.boss
        self.fields['boss'].queryset = Hitmen.objects.filter(is_boss=True, user__is_active=True)
        self.fields['hitmens'].queryset = Hitmen.objects.filter(
            user__is_active=True
        ).exclude(Q(**{'user__id': 1}) | Q(**{'is_boss': True}))
