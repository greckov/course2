from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.blog.models import Post


class IndexView(ListView):
    model = Post
    template_name = 'index.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_view.html'
