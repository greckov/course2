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
    def post(self, request: HttpRequest, post_pk: int) -> HttpResponse:
        if not request.POST.get('content'):
            return JsonResponse({'error': '`content` field is required'})

        if parent_id := request.POST.get('parent_id'):
            parent = get_object_or_404(Comment.objects.only('id'), id=parent_id)
        else:
            parent = None

        Comment.objects.create(
            created_by=request.user,
            content=request.POST['content'],
            post=get_object_or_404(Post.objects.only('id'), id=post_pk),
            parent=parent
        )

        return JsonResponse({'message': 'ok'}, status=201)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        return context
