from django.contrib import admin

from .models import Author, Category, Post, Comment
# from .forms import PostForm
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('heading', 'category_type', 'author')
    list_filter = ('categoryPost', 'category_type', 'author')
    search_fields = ('heading', 'category_type')
    actions = []


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_post', 'comment_user', 'content_comment', 'date_time_create')
    list_filter = ('comment_post', 'comment_user')
    search_fields = ('content_comment', 'comment_user')
    actions = []


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_user', 'ratting_author', 'author_content')
    list_filter = ('author_user', 'ratting_author', 'author_content__heading')
    search_fields = ('ratting_author','author_content__heading')
    actions = []


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', 'subcsribers')
    search_fields = ('name',)
    actions = []


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
