# -*- encoding: utf-8 -*-

from django.urls import path
from apps.transitions.views import TransitionView

app_name = "transitions"

urlpatterns = (
    path(
        route="transition/<slug:transition>/<slug:app>/<slug:model>/<int:pk>/",
        view=TransitionView.as_view(),
        name="transition",
    ),
)
