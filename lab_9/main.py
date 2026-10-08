import sys
import os
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from django.shortcuts import render
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY='Max_very_secret_key',
    ROOT_URLCONF=__name__,
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
        },
    ]
)


def index(request):
    return render(request, 'index.html')

def resume(request):
    return render(request, 'resume.html')

urlpatterns = [
    path('', index),
    path('resume/', resume),
    re_path(r'^img/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, 'img')}),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)