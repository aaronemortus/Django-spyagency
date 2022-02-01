from django import forms
from django.contrib.auth.forms import UserCreationForm
from extra_views import InlineFormSetFactory

from .models import User, Lackey


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class':'input', 'placeholder': 'Email Address'
                }
            ),

        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)


class LackeyForm(forms.ModelForm):
    class Meta:
        model = Lackey
        fields = ('manager',)

    def __init__(self, *args, **kwargs):
        super(LackeyForm, self).__init__(*args, **kwargs)
        self.fields['manager'].required = True
        for field in self.fields.values():
            field.error_messages = {'required':'This field is required.'}
