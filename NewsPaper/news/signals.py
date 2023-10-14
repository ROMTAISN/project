# @receiver(post_save, sender=Post)
# def product_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.categoryPost
#     ).values_list('email', flat=True)
#     subject = f'Новая новость в категории {instance.categoryPost}'
#
#     text_content = (
#         f'Заголовок: {instance.heading}\n'
#         f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Заголовок: {instance.heading}<br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на новость</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()



# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.categoryPost.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subcsribers.all()
#         subscribers = [s.email for s in subscribers]
#
#         def send_notifications(preview, pk, heading, subscribers):
#             html_content = render_to_string(
#                 'post_created_email.html',
#                 {
#                     'text': preview,
#                     'link': f'{settings.SITE_URL}/posts/{pk}'
#                 }
#             )
#             for subscriber in subscribers:
#                 msg = EmailMultiAlternatives(
#                     subject=heading,
#                     body='',
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     to=[subscriber],
#                 )
#
#                 msg.attach_alternative(html_content, 'text/html')
#                 msg.send()
#
#         send_notifications(instance.preview(), instance.pk, instance.heading, subscribers)
