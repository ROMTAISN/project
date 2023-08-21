from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        all_users = Group.objects.get(name='all_users')
        user.groups.add(all_users)
        return user
