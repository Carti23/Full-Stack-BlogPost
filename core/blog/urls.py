from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.MainView, name='MainView'),
    path('post/<int:pk>', views.PostDetailView, name='PostDetailView'),
    path('post/create', views.PostCreateView.as_view(), name='PostCreateView'),
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='PostEditView'),
    path('myposts/', views.MyArticlesView, name='MyArticlesView'),
    path('likepost/<int:pk>', views.LikePost, name='LikePost'),
    path('noaccess/', views.NoAccess, name='NoAccess'),
    path('delete/<int:pk>/', views.delete_blog_view, name='delete-blog'),
]
