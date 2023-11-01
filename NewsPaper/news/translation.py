from .models import Category, Post, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('heading', 'content' )


@register(Comment)
class PostTranslationOptions(TranslationOptions):
    fields = ('content_comment',)
