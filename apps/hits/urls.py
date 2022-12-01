# -*- encoding: utf-8 -*-

from django.urls import path
from apps.hits import views
from apps.hits.views import (
    HitListView,
    HitCreateView,
    HitDetailView,
    HitUpdateView,
    HitmenListView,
    HitmenDetailView,
    GroupListView,
    GroupCreateView,
    GroupDetailView
)

app_name = 'hit'

urlpatterns = [
    path('', views.index, name='home'),
    path(route='hits/', view=HitListView.as_view(), name='hit-list'),
    path(route='hits/create', view=HitCreateView.as_view(), name='hit-create'),
    path(route='hits/<int:pk>/update', view=HitUpdateView.as_view(), name='hit-update'),
    path(route='hits/<int:pk>', view=HitDetailView.as_view(), name='hit-detail'),
    path(route='hitmens', view=HitmenListView.as_view(), name='hitmen-list'),
    path(route='hitmens/<int:pk>', view=HitmenDetailView.as_view(), name='hitmen-detail'),
    path(route='groups', view=GroupListView.as_view(), name='group-list'),
    path(route='groups/create', view=GroupCreateView.as_view(), name='group-create'),
    path(route='groups/<int:pk>', view=GroupDetailView.as_view(), name='group-detail'),
]
