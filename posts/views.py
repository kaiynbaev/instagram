import random
from django.db.models import F
from django.db.models import Count

from django_filters import rest_framework as filters
from rest_framework import filters as r_filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Post, Like, Comment, Notification
from .serializers import (PostSerializer, LikeSerializer, CommentSerializer, 
                          NotificationSerializer, NotificationUpdateSerializer)

# Create your views here.


class MainPage(APIView):
    
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
        
    def get(self, *args, **kwargs):
        my_subscriptions_id = self.request.user.profile.follows.values_list(
            'id', flat=True
        )
        limit = self.request.GET.get('limit')
        offset = self.request.GET.get('offset')
        
        if limit is not None and limit.isdigit():
            limit = int(limit)
        else:
            limit = 20
            
        if offset is not None and offset.isdigit():
            offset = int(offset)
        else:
            offset = 0
            
        posts = Post.objects.filter(
            profile__id__in=my_subscriptions_id
        ).order_by('-create_date').values(
                'id',
                'image',
                'description',
                'update_date',
                username=F('profile__user__username')
                ).annotate(
                    likes=Count('likes')
                )[offset:limit]
        random.shuffle(
            shuffle_list := list(posts)
        )
        return Response(
            data=shuffle_list,
            status=status.HTTP_200_OK
        )


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (filters.DjangoFilterBackend, r_filters.SearchFilter)
    filterset_fields = ('profile__id',)
    search_fields = ('description',)

    
    def perform_create(self, serializer):
        return serializer.save(
            profile=self.request.user.profile
        )
        
        
class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author__id',)

    
    def perform_create(self, serializer):
        like = Like.objects.filter(
            post=serializer.validated_data['post'],
            author=serializer.validated_data['post'].profile,
        ).first()
        if like is not None:
            like.delete()
            return
        return serializer.save(
            author=self.request.user.profile
        )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author__id', 'post__id')
    
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user.profile
        )


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('from_profile__id', 'to_profile__id', 'is_view')
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action in 'update':
            return NotificationUpdateSerializer
        elif self.action == 'partial_update':
            return NotificationUpdateSerializer
        return NotificationSerializer
