from django.contrib import admin
from .models import Task, Topic

class TaskAdmin(admin.ModelAdmin):
    fields = ('category','title', 'description','date','topic','author','subtasks','prio','assigned_clients',)
    list_display = ('title','date','author', 'category','topic',)
    search_fields = ('title','author','category','topic','date',)

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'date','author','color',)
    list_display = ('title', 'date','author','color',)
    search_fields = ('title',)

admin.site.register(Task, TaskAdmin)
admin.site.register(Topic, TopicAdmin)