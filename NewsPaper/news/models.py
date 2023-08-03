from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
# Create your models here.

class Author(models.Model):
    author_user = models.OneToOneField(User, verbose_name='Имя автора', on_delete=models.CASCADE)
    ratting_author = models.SmallIntegerField(default=0, verbose_name='Рейтинг автора')

    def update_rating(self):
        rat_post = self.post_set.all().aggregate(postRating=Sum('ratting_post'))
        rat_p = 0
        rat_p += rat_post.get('postRating')


        rat_comment = self.author_user.comment_set.all().aggregate(commentRating=Sum('ratting_comment'))
        rat_c = 0
        rat_c += rat_comment.get('commentRating')

        self.ratting_author = rat_p * 3 + rat_c
        self.save()

    def __str__(self):
        return f'Автор: {self.author_user.username} Рейтинг: {self.ratting_author}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')
    namePost = models.ManyToManyField('Post', through='PostCategory')

    def __str__(self):
        return self.name.title()


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS, verbose_name='Категория')
    date_time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    categoryPost = models.ManyToManyField('Category', through='PostCategory', )
    heading = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    ratting_post = models.SmallIntegerField(default=0, verbose_name='Рейтинг поста')

    def like(self):
        self.ratting_post += 1
        self.save()

    def dislike(self):
        self.ratting_post -= 1
        self.save()

    def preview(self):
        return f'{self.content[:123]}...'

    def __str__(self):
        return f'{self.heading}. Автор: {self.author.author_user.username} Рейтинг статьи: {self.ratting_post}'


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_comment = models.TextField()
    date_time_create = models.DateTimeField(auto_now_add=True)
    ratting_comment = models.SmallIntegerField(default=0)

    def like(self):
        self.ratting_comment += 1
        self.save()

    def dislike(self):
        self.ratting_comment -= 1
        self.save()
    def __str__(self):
        return self.content_comment
