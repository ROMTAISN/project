from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    heading = forms.CharField(max_length=40)
    content = forms.CharField(min_length=20)
    class Meta:
        model = Post
        fields = [
            'heading',
            'author',
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
            'author',
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