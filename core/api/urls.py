from django.urls import path, include
from .views import * 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('posts/', PostApiView.as_view(), name='all-create-posts'),
    path('post/<int:pk>/', PostApiDetailView.as_view(), name='deatil-post'),
    path('users/', UserApiView.as_view(), name='user-list'),
    path('categories/', CategoryApiView.as_view(), name='category-list-create'),
    path('comments/', CommentApiView.as_view(), name='comment-list-create'),
    path('register/', register, name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('logout/', Logout, name='logout'),
]
