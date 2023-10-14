from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все посты из выбранной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
    def handle(self, *args, **options):
        answer = input(f'Вы точно хотите удалить все посты из категории {options["category"]}? Да/Нет: ')
        # self.stdout.readable()
        # self.stdout.write('Выберете категорию:')
        # cat = set(Post.objects.values_list('categoryPost__name'))
        # print(cat)
        # category = input()
        # self.stdout.write(f'Вы точно хотите удалить все посты из категории {category}? Да/Нет')
        # answer = input()
        if answer == 'Да' or answer == 'да':
            try:
                category = Category.objects.get(name=options['category'])
                Post.objects.filter(categoryPost=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Из категории {category.name} удалены все посты!'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория {options["category"]} не найдена!'))
                return
        else:
            self.stdout.write(self.style.ERROR('Отказано в доступе!'))

