import datetime
from .models import Post, Category
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_msg_every_wick():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_creation__gte=last_week)
    categories = set(posts.values_list('postCategory__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))
    html = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='test@yandex.ru',
        to=subscribers
    )

    msg.attach_alternative(html, 'text/html')
    msg.send()


@shared_task
def send_msg(preview, pk, title, subscribers_email):

    html_content = render_to_string(
        'mail/new_post.html',
        {
            'text': preview,
            'link': f'127.0.0.1:8000/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='test@yandex.ru',
        to=subscribers_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()