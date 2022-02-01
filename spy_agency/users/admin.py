from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User, Manager, Lackey


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ( 'email', 'username','get_group', )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('groups',)}),
    )

    def get_group(self, obj):
        """
        Get groups to access to admin front (bigboss, manager and hitman)
        """
        return [g.name for g in obj.groups.all()]

    get_group.short_description = 'Groups'


class LackeyInline(admin.StackedInline):
    model = Lackey


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager',)
    inlines = [LackeyInline,]


@admin.register(Lackey)
class LackeyAdmin(admin.ModelAdmin):
    list_display = ('lackey', 'manager',)
