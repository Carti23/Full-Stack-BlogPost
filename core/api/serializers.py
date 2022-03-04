from rest_framework import serializers
from account.models import Profile
from blog.models import *

"""Post Serialzer"""
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


"""User Serialzer"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

"""Category Serializer"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

"""Comments Serializer"""
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

"""Register Serializer"""
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        
    """finction which create a user"""
    def create(self, validate_data):
        user = User.objects.create_user(validate_data['username'], validate_data['email'], validate_data['password'])

        return user

"""Change Password Serializer"""
class ChangePasswordSerializer(serializers.ModelSerializer):
    model = User

    id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
