from django import forms
from django.forms import Select
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment, Author


# class PostForm(forms.ModelForm):
#     heading = forms.CharField(max_length=40)
#     content = forms.CharField(min_length=20)
#
#     class Meta:
#         model = Post
#         widgets = {
#             'categoryPost': Select(),
#         }
#         fields = [
#             'heading',
#             'category_type',
#             'categoryPost',
#             'content',
#         ]
#
#     def clean(self):
#         cleaned_data = super().clean()
#         heading = cleaned_data.get('heading')
#         content = cleaned_data.get('content')
#
#         if heading == content:
#             raise ValidationError('Текст не должен быть идентичен названию.')
#         return cleaned_data


class NewsForm(forms.ModelForm):
    heading = forms.CharField(max_length=40)
    content = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'heading',
            'categoryPost',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get('heading')
        content = cleaned_data.get('content')

        if heading == content:
            raise ValidationError('Текст не должен быть идентичен названию.')
        return cleaned_data


class ArticleForm(forms.ModelForm):
    heading = forms.CharField(max_length=40)
    content = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'heading',
            'categoryPost',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get('heading')
        content = cleaned_data.get('content')

        if heading == content:
            raise ValidationError('Текст не должен быть идентичен названию.')
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content_comment','parent']

        labels = {
            'content_comment': _(''),
        }

        widgets = {
            'content_comment' : forms.TextInput(),
        }
