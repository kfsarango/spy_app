# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.db.models import QuerySet, Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.hits.choices import HitStatusChoices
from apps.hits.forms import HitForm, GroupForm, HitInactiveAssignedForm
from apps.hits.models import Hit, Hitmen, Group
from core.settings import BIG_BOSS_ID


# Create your views here.
class AccessBothBoss:
    only_big_boss = False

    def get(self, request, *args, **kwargs):
        user = request.user

        is_big_boss = user.id == BIG_BOSS_ID
        is_boss = user.hitmen.is_boss

        if self.only_big_boss:
            if not is_big_boss:
                raise PermissionDenied
        else:
            if not (is_big_boss or is_boss):
                raise PermissionDenied

        return super().get(request, *args, **kwargs)


class BaseListView:
    search_param = None

    def get_context_data(self, **kwargs):
        data = {'search_param': self.search_param}
        return super().get_context_data(**data)

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        # Set search param
        self.search_param = self.request.GET.get('search', None)

        return queryset


def index(request):
    html_template = loader.get_template('hits/index.html')
    return HttpResponse(html_template.render({}, request))


class HitmenListView(AccessBothBoss, BaseListView, ListView):
    model = Hitmen
    paginate_by = 10
    template_name = 'hits/hitmen/list_hitmen.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        hitmen = self.request.user.hitmen
        if hitmen.is_boss:
            lackeys_id = hitmen.get_all_lackeys_ids()
            queryset = queryset.filter(id__in=lackeys_id)

        if self.search_param:
            qs = Q(**{'user__first_name__icontains': self.search_param}) | Q(
                **{'user__last_name__icontains': self.search_param}
            )
            queryset = queryset.filter(qs)

        return queryset


class HitmenDetailView(DetailView):
    model = Hitmen
    template_name = 'hits/hitmen/detail_hitmen.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        hitmen = self.get_object()

        is_valid_boss = hitmen.id in user.hitmen.get_all_lackeys_ids()
        is_owner = user.hitmen.id == hitmen.id
        if not (is_valid_boss or is_owner or user.id == BIG_BOSS_ID):
            raise PermissionDenied

        return super().get(request, *args, **kwargs)


class HitListView(BaseListView, ListView):
    model = Hit
    paginate_by = 10
    template_name = 'hits/hit/list_hit.html'

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()

        # Filtering by assignations hits
        if user.hitmen.is_boss:
            lackeys_id = user.hitmen.get_all_lackeys_ids()
            lackeys_id.append(user.hitmen.id)
            queryset = queryset.filter(assigned_to__in=lackeys_id)
        elif user.id != BIG_BOSS_ID:
            queryset = queryset.filter(assigned_to=user.hitmen)

        # Filtering by search key
        if self.search_param:
            qs = Q(**{'target_name__icontains': self.search_param}) | Q(
                **{'assigned_to__user__first_name__icontains': self.search_param}
            ) | Q(
                **{'assigned_to__user__last_name__icontains': self.search_param}
            )
            queryset = queryset.filter(qs)

        return queryset.order_by('-created_date')


class HitCreateView(AccessBothBoss, CreateView):
    model = Hit
    form_class = HitForm
    template_name = 'layouts/form.html'

    def get_success_url(self):
        return reverse('hit:hit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'New Hit'
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.assigned_by = user.get_full_name()
        self.object.save()

        return super().form_valid(form)


class HitUpdateView(UpdateView):
    model = Hit
    form_class = HitForm
    template_name = 'layouts/form.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        hit = self.get_object()

        is_valid_boss = hit.assigned_to.id in user.hitmen.get_all_lackeys_ids()
        if not (is_valid_boss or user.id == BIG_BOSS_ID):
            raise PermissionDenied
        elif hit.state != HitStatusChoices.ASSIGNED:
            messages.info(self.request, 'Hit cannot be updated.')
            return redirect(reverse('hit:hit-detail', kwargs={'pk': hit.id}))
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('hit:hit-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'Edit Hit'
        return context

    def get_form(self, form_class=None):
        form_class = self.get_form_class()

        # Assigned hitmen is inactive - Change form class to edit
        if not self.get_object().assigned_to.user.is_active:
            form_class = HitInactiveAssignedForm

        return form_class(**self.get_form_kwargs())


class HitDetailView(DetailView):
    model = Hit
    template_name = 'hits/hit/detail_hit.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        hit = self.get_object()
        is_owner = user.hitmen.id == hit.assigned_to.id
        is_valid_boss = hit.assigned_to.id in user.hitmen.get_all_lackeys_ids()
        if not (is_owner or is_valid_boss or user.id == BIG_BOSS_ID):
            raise PermissionDenied

        return super().get(request, *args, **kwargs)


class GroupListView(AccessBothBoss, BaseListView, ListView):
    model = Group
    paginate_by = 10
    template_name = 'hits/group/list_group.html'
    only_big_boss = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_param:
            qs = Q(**{'name__icontains': self.search_param}) | Q(
                **{'boss__user__first_name__icontains': self.search_param}
            ) | Q(
                **{'boss__user__last_name__icontains': self.search_param}
            )
            queryset = queryset.filter(qs)

        return queryset


class GroupCreateView(AccessBothBoss, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'layouts/form.html'
    only_big_boss = True

    def get_success_url(self):
        return reverse('hit:group-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'New Group'
        return context


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'layouts/form.html'

    def get_success_url(self):
        return reverse('hit:hit-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'Edit Group'
        return context


class GroupDetailView(AccessBothBoss, DetailView):
    model = Group
    template_name = 'hits/group/detail_group.html'
    only_big_boss = True
