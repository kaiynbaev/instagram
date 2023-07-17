import random
from django.db.models import F
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer

# Create your views here.


class MainPage(APIView):
    
    serializer_class = PostSerializer
    
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
    
    def perform_create(self, serializer):
        return serializer.save(
            profile=self.request.user.profile
        )
        
        
class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(
            profile=self.request.user.profile
        )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(
            profile=self.request.user.profile
        )
