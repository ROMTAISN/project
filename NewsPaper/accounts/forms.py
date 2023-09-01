from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        all_users = Group.objects.get(name='all_users')
        user.groups.add(all_users)

        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/posts/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()

        return user
