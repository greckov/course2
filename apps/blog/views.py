from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import QuerySet, Count, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from apps.blog.models import Post, Category, Comment, PostReaction


class IndexView(ListView):
    code_name = 'index'
    template_name = 'index.html'
    queryset = Post.objects.all_with_reactions()

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
        context['user_reacted'] = self.object.reactions.filter(reacted_by=self.request.user).exists()
        context.update(self.object.reactions.aggregate(
            likes=Count('id', filter=Q(reaction_type=PostReaction.LIKE)),
            dislikes=Count('id', filter=Q(reaction_type=PostReaction.DISLIKE)),
        ))
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

        with transaction.atomic():
            comment = Comment.objects.create(
                created_by=request.user,
                content=request.POST['content'],
                post=get_object_or_404(Post.objects.only('id'), id=post_pk),
                parent=parent
            )

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Comment).id,
                object_id=comment.id,
                object_repr=str(comment),
                action_flag=ADDITION
            )

        return JsonResponse({'message': 'ok'}, status=201)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all_with_reactions().filter(categories=self.object)
        return context


class SaveUserReactionView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, post_pk: int) -> HttpResponse:
        post = get_object_or_404(Post, pk=post_pk)

        if post.user_already_reacted(request.user.id):
            return JsonResponse({'error': 'Current user is already reacted on this post'})

        reaction_type = request.POST.get('reaction')

        if reaction_type not in ('like', 'dislike'):
            return JsonResponse({'error': '`reaction` field should have `like` or `dislike` value'}, status=400)

        PostReaction.objects.create(
            post=post,
            reaction_type=getattr(PostReaction, reaction_type.upper()),
            reacted_by=request.user
        )
        return JsonResponse({'message': 'ok'}, status=201)

