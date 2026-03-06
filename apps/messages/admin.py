from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'channel',
        'content_preview',
        'parent_message',
        'created_at',
    ]
    list_filter = ['channel', 'created_at']
    search_fields = ['content', 'author__email', 'channel__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Message Content', {
            'fields': ('content',)
        }),
        ('Relationships', {
            'fields': ('author', 'channel', 'parent_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        """Show first 50 simbol message"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    content_preview.short_description = 'Content'