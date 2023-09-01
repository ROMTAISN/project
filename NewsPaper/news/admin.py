
from django.contrib import admin
from .models import Post, Category, Author, PostCategory

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.author = request.user
#         super(PostAdmin, self).save_model(
#         request=request,
#         obj=obj,
#         form=form,
#         change=change
#         )