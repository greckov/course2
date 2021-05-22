from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from apps.blog.models import Post, Category, Comment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.filter(parent__isnull=True)
        return context


class CategoryListView(ListView):
    code_name = 'category_list'
    model = Category
    template_name = 'category_list.html'


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not request.POST.get('content'):
            return JsonResponse({'error': '`content` field is required'})

        Comment.objects.create(
            created_by=request.user,
            content=request.POST['content'],
            post=get_object_or_404(Post.objects.only('id'), id=self.kwargs['post_pk'])
        )

        return JsonResponse({'message': 'ok'}, status=201)
