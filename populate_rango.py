import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial', 'url': 'https://docs.python.org/3/tutorial/', 'views': 128},
        {'title': 'Real Python', 'url': 'https://realpython.com/', 'views': 64},
        {'title': 'Django Documentation', 'url': 'https://docs.djangoproject.com/', 'views': 32},
    ]

    django_pages = [
        {'title': 'Django Official Site', 'url': 'https://www.djangoproject.com/', 'views': 128},
        {'title': 'Django Tutorial', 'url': 'https://docs.djangoproject.com/en/2.2/intro/', 'views': 64},
        {'title': 'Django Girls Tutorial', 'url': 'https://tutorial.djangogirls.org/en/', 'views': 32},
    ]

    other_pages = [
        {'title': 'MDN Web Docs', 'url': 'https://developer.mozilla.org/', 'views': 64},
        {'title': 'Stack Overflow', 'url': 'https://stackoverflow.com/', 'views': 32},
        {'title': 'GitHub', 'url': 'https://github.com/', 'views': 16},
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Resources': {'pages': other_pages, 'views': 32, 'likes': 16},
    }

    for cat_name, cat_data in cats.items():
        c = add_cat(cat_name, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])

    
    for c in Category.objects.all():
        print(f'- {c} (views={c.views}, likes={c.likes}, slug={c.slug})')
        for p in Page.objects.filter(category=c):
            print(f'  - {p} (views={p.views}) -> {p.url}')


def add_cat(name, views=0, likes=0):
    c, created = Category.objects.get_or_create(name=name)
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(category, title, url, views=0):
    p, created = Page.objects.get_or_create(category=category, title=title)
    p.url = url
    p.views = views
    p.save()
    return p


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
