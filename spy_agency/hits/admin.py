from django.contrib import admin

from .models import Hit


@admin.register(Hit)
class HitAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'assignee', 'target', 'status')
