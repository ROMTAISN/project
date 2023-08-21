from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class AuthorList(ListView):
    model = Author
    ordering = 'author_user'
    template_name = 'authors.html'
    context_object_name = 'authors'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


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
        # form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

# временный класс, для проверки прав доступа
# class PostCreate(PermissionRequiredMixin, CreateView):
#     permission_required = ('news.add_post',)
#     form_class = PostForm
#     model = Post
#     template_name = 'post_create.html'
#
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.category_type = 'NW'
#         # form.instance.author = self.request.user.author
#         return super().form_valid(form)