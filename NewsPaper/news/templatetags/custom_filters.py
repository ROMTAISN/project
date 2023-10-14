from django import template


register = template.Library()


FORBIDDEN_WORDS = [
    'Хуй', 'хуй', 'Пизда', 'пизда', 'Пидорас', 'пидорас', 'Ебать', 'ебать', 'Пидор', 'пидор',
    'Пидоры', 'пидоры', 'Гандоны', 'гандоны', 'Уёбки', 'уёбки', 'Уебки', 'уебки', 'Уёбок',
    'уёбок', 'Уебок', 'уебок', 'Пидорасы', 'пидорасы', 'пиздец', 'ебаный'
]


@register.filter(name='censor')
def currency(value):
    if value is not str:
        rec = value.split()
        for w in FORBIDDEN_WORDS:
            for idx, word in enumerate(rec):
                if w in word:
                    rec[idx] = '*' * (len(word) - 2)
                    rec[idx] = word[0] + rec[idx] + word[-1]
                    value = ' '.join(rec)
        return value
    else:
        return f'{TypeError} - фильтр доступен только для строк.'
