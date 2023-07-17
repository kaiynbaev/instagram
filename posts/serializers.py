from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        exclude = ['profile']


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        exclude = ['profile']
        
        
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        exclude = ['profile']
