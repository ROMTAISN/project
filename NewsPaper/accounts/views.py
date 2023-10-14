# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView
from .forms import CustomSignupForm, AccountForm
from .models import Personal

class SignUp(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

    # пробуем связать пользователя с моделью Автор

class AccountDetail(DetailView):
    model = Personal
    template_name = 'account.html'
    context_object_name = 'account'

    def get_queryset(self):
        # self.user = User.objects.values_list('username').filter(id=self.request.user.id)
        queryset = Personal.objects.filter(user=self.request.user.id)
        return queryset
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(user=self.request.user.id)
    #     return queryset


class AccountUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('account.change_account',)
    form_class = AccountForm
    model = Personal
    template_name = 'account_update.html'

    def get_queryset(self):
        queryset = Personal.objects.filter(user=self.request.user.id)
        return queryset
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
