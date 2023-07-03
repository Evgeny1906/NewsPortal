from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email

def new_post_subckription(instance):
    template = 'mail/new_post.html'
    for category in instance.postCategory.all():
        email_subject = f'New Post in category {category}'

        user_email = get_subscriber(category)
        print(user_email)
        html = render_to_string(
        template_name = template,
            context={'category': category, 'post': instance}


        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email='test@yandex.ru',
            to=user_email,
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()