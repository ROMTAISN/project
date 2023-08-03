from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Author
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'


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