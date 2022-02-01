from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout, views
from django.views.generic import RedirectView, edit, list
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from extra_views import UpdateWithInlinesView

from .forms import UserRegistrationForm, UpdateUserForm, LackeyForm
from .models import User, Manager, Lackey
from core.helpers import get_manager_lackeys


class LoginView(views.LoginView):
    template_name = 'user/login.html'
    next_page = None

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        return reverse('hits:list')


class LogoutView(RedirectView):
    pattern_name = 'users:login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignUpView(edit.CreateView):
    template_name = 'user/register.html'
    success_url = '/login'
    form_class = UserRegistrationForm

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email.split('@')[0]        
        messages.success(
            self.request,
            'User " %s "  has been successfully created.' % user
        )
        return super().form_valid(form)


class UsersListView(LoginRequiredMixin, GroupRequiredMixin, list.ListView):
    group_required = ('bigboss', 'manager',)
    template_name = 'user/users_list.html'
    paginate_by = 10
    model = User
    login_url = "/login"

    def get_queryset(self):
        if not self.request.user.is_superuser:
            group = self.request.user.groups.get().name
            if group == 'manager':
                manager = Manager.objects.filter(
                                            manager__email=self.request.user)
                lackeys = Lackey.objects.filter(manager__in=manager)
                users_list = lackeys
            elif group == 'bigboss':
                users_list = User.objects.all().exclude(is_superuser=True)
                users_list = users_list.exclude(email=self.request.user)
        else:
            users_list = User.objects.all().exclude(is_superuser=True)
        return users_list.order_by('id')


class UserUpdate(LoginRequiredMixin, GroupRequiredMixin, edit.UpdateView):
    group_required = ('bigboss', 'manager',)
    template_name = 'user/user_update.html'
    form_class = UpdateUserForm
    model = User
    login_url = "/login"

    def get_form_kwargs(self):
        kwargs = super(UserUpdate, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        manager = Manager.objects.filter(manager__email=self.get_object())
        manager = manager.values_list('id', flat=True)
        lackeys = Lackey.objects.filter(manager__in=manager)
        context['lackeys_list'] = lackeys
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            'User "%s"  has been successfully updated.' % user.username
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:hitmen')


class UpdateLackeyView(LoginRequiredMixin, GroupRequiredMixin, edit.UpdateView):
    group_required = ('bigboss', 'manager',)
    model = Lackey
    form_class = LackeyForm
    template_name = 'user/update_lackey.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateLackeyView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

    def get_success_url(self):
        return reverse('users:hitmen')

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            'User "%s"  has been successfully updated.' % user.lackey.username
        )
        return super().form_valid(form)
