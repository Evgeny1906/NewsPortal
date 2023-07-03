from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .tasks.basic import new_post_subckription


@receiver(m2m_changed, sender=PostCategory)
def news_create(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subckription(instance)

