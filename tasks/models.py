from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import JSONField
from contacts.models import Contact

class Topic(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True) 
    date = models.DateField(default=timezone.now().date)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Task(models.Model):
    category = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(default=timezone.now().date)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topics', blank=True, null=True)
    subtasks = JSONField(blank=True, null=True)
    prio = models.CharField(max_length=30, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    assigned_clients = models.ManyToManyField(Contact, related_name='tasks', blank=True)
