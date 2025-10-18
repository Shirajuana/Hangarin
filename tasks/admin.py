from django.contrib import admin
from .models import Priority, Category, Task, SubTask, Note

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ("title", "status", "description")
    show_change_link = True
    
    def get_queryset(self, request):
        # Optional: Customize the queryset if needed
        return super().get_queryset(request).select_related('task')

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ("content", "created_at")
    readonly_fields = ("created_at",)
    
    def get_queryset(self, request):
        # Optional: Customize the queryset if needed
        return super().get_queryset(request).select_related('task')

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'priority', 'category', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    # Add fields for the task edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status')
        }),
        ('Categorization & Scheduling', {
            'fields': ('category', 'priority', 'deadline')
        }),
    )
    
    # Add the inlines
    inlines = [SubTaskInline, NoteInline]
    
    # Optional: Add some JavaScript for better date/time pickers
    class Media:
        js = (
            'admin/js/calendar.js',
            'admin/js/admin/DateTimeShortcuts.js',
        )

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent_task_name', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    
    def parent_task_name(self, obj):
        return obj.task.title
    parent_task_name.short_description = 'Parent Task'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['task', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'