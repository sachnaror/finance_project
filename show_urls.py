import os
import django
from django.urls import URLPattern, URLResolver
from django.urls import get_resolver

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_project.settings")
django.setup()

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    for entry in lis:
        if isinstance(entry, URLPattern):
            acc.append(entry.pattern)
        elif isinstance(entry, URLResolver):
            list_urls(entry.url_patterns, acc)
    return acc

if __name__ == "__main__":
    urls = list_urls(get_resolver().url_patterns)
    for url in urls:
        print(url)
