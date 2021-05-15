from django.shortcuts import render
from django.views.generic import ListView

from apps.blog.models import Post


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
