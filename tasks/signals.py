from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Task

@receiver(m2m_changed, sender=Task.assigned_clients.through)
def update_tasks_on_contact_deletion(sender, instance, action, pk_set, **kwargs):
    if action == 'pre_remove':
        Task.objects.filter(assigned_clients__in=pk_set).update(assigned_clients=None)