from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout, views
from django.views.generic import list, edit, CreateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from extra_views import ModelFormSetView

from .models import Hit
from users.models import Manager, Lackey, User
from core.helpers import get_manager_lackeys
from .forms import UpdateHitForm, CreateHitForm, BulkForm


class HitList(LoginRequiredMixin, GroupRequiredMixin, list.ListView):
    group_required = ('bigboss', 'manager', 'hitman')
    template_name = 'hits/hits_list.html'
    paginate_by = 10
    model = Hit
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super(HitList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        order = Hit.objects.all().order_by('-id')
        if not self.request.user.is_superuser:
            group = self.request.user.groups.get().name
            if group == 'hitman':
                list = Hit.objects.filter(assignee=self.request.user)
            elif group == 'manager':
                assignee_list = Hit.objects.filter(assignee=self.request.user)
                creator_list = Hit.objects.filter(creator=self.request.user)
                lackeys = get_manager_lackeys(self.request.user)
                lackeys = User.objects.filter(email__in=lackeys)
                hits_lackeys = Hit.objects.filter(assignee__in=lackeys)
                list = assignee_list.union(creator_list, hits_lackeys)
            elif group == 'bigboss':
                list = Hit.objects.all()
        else:
            list = Hit.objects.all()
        list = list.order_by('-id')
        return list


class HitUpdate(LoginRequiredMixin, GroupRequiredMixin, edit.UpdateView):
    group_required = ('bigboss', 'manager', 'hitman')
    template_name = 'hits/hit_update.html'
    model = Hit
    form_class = UpdateHitForm
    login_url = "/login"

    def get_form_kwargs(self):
        kwargs = super(HitUpdate, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        hit = form.save(commit=False)
        if hit.status == 'failed':
            hit.assignee.is_active = False
            hit.assignee.save()
        messages.success(
            self.request,
            'Hit with id " %s "  has been successfully updated.' % hit.id
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oops. Please, check the required fields.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('hits:list')


class CreateHit(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ('bigboss', 'manager')
    template_name = 'hits/create_hit.html'
    form_class = CreateHitForm
    success_url = '/list'
    login_url = "/login"

    def get_form_kwargs(self):
        kwargs = super(CreateHit, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        hit = form.save(commit=False)
        hit.creator = self.request.user
        group = self.request.user.groups.get().name
        if group == 'manager':
            manager_email = Manager.objects.get(
                                            manager__email=self.request.user)
            lackey_email = User.objects.get(email=hit.assignee)
            lackey = Lackey()
            lackey.manager = manager_email
            lackey.lackey = lackey_email
        else:
            hit.save()
        messages.success(
            self.request,
            'Hit to target " %s "  has been successfully created.' % hit
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oops. Please, check the required fields.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('hits:list')


class BulkHits(LoginRequiredMixin, GroupRequiredMixin, ModelFormSetView):
    group_required = ('bigboss', 'manager')
    model = Hit
    template_name = 'hits/bulk_hits.html'
    form_class = BulkForm
    success_url = '/list'
    factory_kwargs = {'extra': 0}


    def get_queryset(self):
        if not self.request.user.is_superuser:
            group = self.request.user.groups.get().name
            if group == 'manager':
                assignee_list = Hit.objects.filter(assignee=self.request.user)
                creator_list = Hit.objects.filter(creator=self.request.user)
                creator_list = creator_list.filter(status='assigned')
                list = assignee_list.union(creator_list)
            elif group == 'bigboss':
                list = Hit.objects.filter(status='assigned')
        else:
            list = Hit.objects.all()
        return list

    def construct_formset(self):
        formsets = super(BulkHits, self).construct_formset()
        if not self.request.user.is_superuser:
            group = self.request.user.groups.get().name
            lackeys = get_manager_lackeys(self.request.user)
            if group == 'manager':
                users = User.objects.filter(email__in=lackeys)
            elif group == 'bigboss':
                users = User.objects.all().exclude(is_superuser=True)
                users = users.exclude(email=self.request.user)
            for formset in formsets:
                formset.fields['assignee'].queryset = users
        return formsets

    def formset_valid(self, formset):
        formset.save()
        messages.success(self.request,'Hit has been successfully reassigned.')
        return super().formset_valid(formset)

    def formset_invalid(self, formset):
        messages.error(self.request, 'Oops. Please, check the required fields.')
        return super().formset_invalid(formset)

    def get_success_url(self):
        return reverse('hits:list')
