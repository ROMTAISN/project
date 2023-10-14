from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
class Personal(models.Model):
    user = models.OneToOneField(User, verbose_name='Логин', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='Имя')
    surname = models.CharField(max_length=128, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=128, verbose_name='Отчество')
    MAN = 'М'
    WOMAN = 'Ж'
    GENDER_CHOICES = (
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MAN, verbose_name='Пол')
    country = models.CharField(max_length=64, verbose_name='Страна')
    city = models.CharField(max_length=64, verbose_name='Город')
    about_me = models.TextField(verbose_name='О себе')
    group_user = models.ForeignKey(Group,on_delete=models.CASCADE, blank=True, null=True, verbose_name='Группы')