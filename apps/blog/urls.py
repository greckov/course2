from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_view'),
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('post/<int:post_pk>/create_comment/', views.CommentCreateView.as_view(), name='create_comment'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
