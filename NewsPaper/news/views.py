from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.context_processors import csrf, request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django.core.cache import cache
from .models import Post, Author, Category, Comment
from .filters import PostFilter
from .forms import NewsForm, ArticleForm, CommentForm
from .tasks import send_email_task
from django.utils import timezone

import pytz
# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get(self, request):
        current_time = timezone.now()
        context = {
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        }

        return HttpResponse(render(request, 'posts.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/posts/')


# class PostDetail(DetailView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'
#
#     def get_object(self, *args, **kwargs):
#         obj = cache.get(f'post-{self.kwargs["pk"]}', None)
#
#         if not obj:
#             obj = super().get_object(queryset=self.queryset)
#             cache.set(f'post-{self.kwargs["pk"]}', obj)
#         return obj


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        connected_comments = Comment.objects.filter(comment_post=self.get_object())
        number_of_comments = connected_comments.count()
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentForm
        return data

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            print('-----------------------------------------------Reached here')
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                content_comment = comment_form.cleaned_data['content_comment']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None


            new_comment = Comment(content_comment=content_comment, comment_user=self.request.user, comment_post=self.get_object(), parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)


class AuthorList(ListView):
    model = Author
    ordering = 'author_user'
    template_name = 'authors.html'
    context_object_name = 'authors'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'

    def get_queryset(self):
        self.author = Author.objects.values_list('author_user').filter(id=self.kwargs['pk'])
        queryset = Post.objects.filter(author=self.author).order_by('-date_time_create')
        return queryset


class NewsList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Фильтрация постов с параметром category_type = 'NW'
        queryset = super().get_queryset()
        queryset = queryset.filter(category_type='NW')
        return queryset


class ArticleList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'article.html'
    context_object_name = 'article'
    paginate_by = 10

    def get_queryset(self):
        # Фильтрация постов с параметром category_type = 'AR'
        queryset = super().get_queryset()
        queryset = queryset.filter(category_type='AR')
        return queryset


class SearchList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        form.instance.author = self.request.user.author
        post.save()
        send_email_task.delay(post.pk)
        return super().form_valid(form)
    #
    # def save_model(self, request, obj, form, change):
    #     obj.author = request.user
    #     super().save_model(request, obj, form, change)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        form.instance.author = self.request.user.author
        post.save()
        send_email_task.delay(post.pk)
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_update.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user.author)
        return queryset


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user.author)
        return queryset


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user.author)
        return queryset


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user.author)
        return queryset


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(author_user=user)
    return redirect('/posts/news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categoryPost=self.category).order_by('-date_time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subcsribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subcsribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
@require_http_methods
def add_comment(request, post_id):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, id=post_id)

        if form.is_valid():
            comment = Comment()
            comment.path = []
            comment.comment_post = post
            comment.comment_user = request.user
            comment.content_comment = form.cleaned_data['comment_area']
            comment.save()

            try:
                comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
                comment.path.append(comment.id)
            except ObjectDoesNotExist:
                comment.path.append(comment.id)

            comment.save()
        return redirect(post.get_absolute_url())
