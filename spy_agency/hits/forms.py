import re
from django import forms
from django.forms import widgets

from .models import Hit
from users.models import User, Manager, Lackey
from core.helpers import get_manager_lackeys


class UpdateHitForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ('status', 'assignee',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UpdateHitForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'This field is required.'}
            field.widget.attrs['class'] = 'form-control'
        if self.user.groups.filter(name__iexact='manager'):
            lackeys = get_manager_lackeys(self.user)
            lackeys = User.objects.filter(email__in=list(lackeys))
            self.fields['assignee'].queryset = lackeys

    def clean_assignee(self):
        assignee = self.cleaned_data['assignee']
        if assignee.lackey:
            is_active = assignee.lackey.lackey.is_active
        elif assignee.manager:
            is_active = assignee.manager.manager.is_active
        if not is_active:
            raise forms.ValidationError('This user is not active (or dead)')
        return assignee


class CreateHitForm(forms.ModelForm):
    class Meta:
        model = Hit
        exclude = ('creator', 'status',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateHitForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'This field is required.'}
            field.widget.attrs['class'] = 'form-control'
        if self.user.groups.filter(name__iexact='manager'):
            lackeys = get_manager_lackeys(self.user)
            lackeys = lackeys.filter(lackey__is_active=True)
            lackeys = User.objects.filter(email__in=list(lackeys))
            self.fields['assignee'].queryset = lackeys
        else:
            users = User.objects.all().exclude(is_superuser=True)
            users = users.exclude(email=self.user)
            self.fields['assignee'].queryset = users


class BulkForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ('assignee',)

    def __init__(self, *args, **kwargs):
        super(BulkForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'This field is required.'}
            field.widget.attrs['class'] = 'form-control'
            field.label = ''

    def clean_assignee(self):
        assignee = self.cleaned_data['assignee']
        if assignee.lackey:
            is_active = assignee.lackey.lackey.is_active
        elif assignee.manager:
            is_active = assignee.manager.manager.is_active
        if not is_active:
            raise forms.ValidationError('This user is not active (or dead)')
        return assignee
