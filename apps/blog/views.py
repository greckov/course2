from django.db.models import QuerySet
from django.views.generic import ListView, DetailView

from apps.blog.models import Post, Category


class IndexView(ListView):
    code_name = 'index'
    model = Post
    template_name = 'index.html'

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()

        if query := self.request.GET.get('q'):
            queryset = queryset.filter(title__icontains=query)

        return queryset


class PostDetailView(DetailView):
    code_name = 'post_view'
    model = Post
    template_name = 'post_view.html'


class CategoryListView(ListView):
    code_name = 'category_list'
    model = Category
    template_name = 'category_list.html'
