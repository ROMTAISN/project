# Generated by Django 4.2.3 on 2023-08-03 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratting_author', models.SmallIntegerField(default=0)),
                ('author_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_type', models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статья')], default='NW', max_length=2)),
                ('date_time_create', models.DateTimeField(auto_now_add=True)),
                ('heading', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('ratting_post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_through', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post_through', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='_category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_comment', models.TextField()),
                ('date_time_create', models.DateTimeField(auto_now_add=True)),
                ('ratting_comment', models.SmallIntegerField(default=0)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
