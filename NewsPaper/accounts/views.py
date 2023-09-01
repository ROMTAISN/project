# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .forms import CustomSignupForm


class SignUp(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

    # пробуем связать пользователя с моделью Автор


# @login_required
# def upgrade_user(request):
#     user = request.user
#     group = Group.objects.get(name='Authors')
#     if not user.groups.filter(name='Authors').exists():
#         group.user_set.add(user)
#
#         from NewsPaper.news.models import Author
#         Author.objects.create(authorUser=User.objects.get(pk=user.id))
#     return redirect('/posts/news')
