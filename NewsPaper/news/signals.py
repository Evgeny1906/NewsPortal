from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_msg
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

# from .tasks.basic import new_post_subckription


@receiver(m2m_changed, sender=PostCategory)
def news_create(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        print(subscribers)
        send_msg.delay(instance.preview(), instance.pk, instance.title, subscribers)

