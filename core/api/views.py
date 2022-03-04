from django.shortcuts import render
from blog.models import *
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from knox.auth import AuthToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout

"""Post API View"""
class PostApiView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


"""Post Detail Api View"""
class PostApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

"""User View API"""
class UserApiView(generics.ListCreateAPIView):
    permissions_classes = (permissions.IsAuthenticated)
    serializer_class = UserSerializer
    queryset = User.objects.all()


"""User Detail Api View"""
class UserDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


"""Category View API"""
class CategoryApiView(generics.ListCreateAPIView):
    permissions_classes = (permissions.IsAuthenticated)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

"""Comment View API"""
class CommentApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


"""helpfu function for registartion"""
def serialize_user(user):
    return {
        "usernme": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

"""Register View API"""
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })

""" Authentication System """
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""Logout Sysytem"""
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Logout(request):
    logout(request)
    return Response('User Logged out successfully')


"""Change Password API View"""
"""Change Password API"""
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if not id.is_valid():
                return False
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
