from datetime import datetime
import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import Post, Category


@shared_task
def send_email_task(pk):
    # try:
    post = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     post = None
    categories = post.categoryPost.all()
    title = post.heading
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subcsribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )
    for subscriber in subscribers_emails:
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_message_every_week():
    subscribers = set(Category.objects.values_list('subcsribers__email', flat=True))
    for sub in subscribers:
        cat = Category.objects.filter(subcsribers__email=sub).values_list('id', flat=True)
        today = datetime.datetime.now()
        last_week = today - datetime.timedelta(days=7)
        posts = Post.objects.filter(date_time_create__gte=last_week)
        relevant_posts = []
        for post in posts:
            cate = post.categoryPost.values_list('id', flat=True)
            if any(c in cate for c in cat):
                relevant_posts.append(post)
        print(relevant_posts)

        html_content = render_to_string(
            'daily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': relevant_posts,
            },
        )
        msg = EmailMultiAlternatives(
            subject='Новости за последние 7 дней в Ваших любимых категориях',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
