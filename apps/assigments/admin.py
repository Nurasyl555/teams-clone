from django.contrib.admin import register,ModelAdmin

from .models import (
    Assignments,
    Assignment_Submissions
)


@register(Assignments)
class AssigmnetsAdmin(ModelAdmin):
    list_display = (
        'team',
        'title',
        'due_data',
        'max_points'
    )
    list_editable = ('max_points',)
    list_filter = ('team_id',)


@register(Assignment_Submissions)
class Assignment_SubmissionsAdmin(ModelAdmin):
    list_display = (
        'assignment',
        'status',
    )
    list_editable = ('status',)
    list_filter = ('status',)
