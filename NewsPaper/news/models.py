from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


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
    # namePost = models.ManyToManyField('Post', through='PostCategory')
    subcsribers = models.ManyToManyField(User, related_name='categories')

    def get_category(self):
        return self.name

    def __str__(self):
        return self.name


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
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS, verbose_name='Тип')
    date_time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    categoryPost = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    heading = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    ratting_post = models.SmallIntegerField(default=0, verbose_name='Рейтинг поста')

    def preview(self):
        return f'{self.content[:123]}...'

    def like(self):
        self.ratting_post += 1
        self.save()

    def dislike(self):
        self.ratting_post -= 1
        self.save()



    def __str__(self):
        return f'{self.heading}. Автор: {self.author.author_user.username} Рейтинг статьи: {self.ratting_post}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class News(Post):
    def __init__(self, *args, **kwargs):
        super(News, self).__init__(*args, **kwargs)
        # Отфильтровываем посты с параметром category_type = 'NW'
        news_post = Post.objects.filter(category_type='NW')
        return news_post


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.heading} | {self.category.name}'


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
