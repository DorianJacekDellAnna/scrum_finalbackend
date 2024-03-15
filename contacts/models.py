from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    initials = models.CharField(max_length=5, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)