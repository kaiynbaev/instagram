from rest_framework import serializers
from .models import Post, Comment, Like, Notification

class PostSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        from_profile = kwargs['profile']
        subscriptions = from_profile.followed_by.all()

        notifications = []
        
        description = self.validated_data['description'][:10]
        for subscription in subscriptions:
            
            notification = Notification(
                from_profile=from_profile,
                to_profile=subscription,
                message=f'Пользователь {from_profile} опубликовал пост {description}!'
            )
            notifications.append(notification)
        Notification.objects.bulk_create(
            notifications
        )
        return super().save(**kwargs)
    
    class Meta:
        model = Post
        exclude = ['profile']


class CommentSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        from_profile = kwargs['author']
        post = self.validated_data['post']
        to_profile = self.validated_data['post'].profile
        notification = Notification(
            from_profile=from_profile,
            to_profile=to_profile,
            message=f'Пользователь {from_profile} написал коментарий на пост {post.description[:10]}!'
        )
        notification.save()
        return super().save(**kwargs)
    
    class Meta:
        model = Comment
        exclude = ['author']
        
        
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        exclude = ['author']
        
    def save(self, **kwargs):
        from_profile = kwargs['author']
        post = self.validated_data['post']
        to_profile = self.validated_data['post'].profile
        notification = Notification(
            from_profile=from_profile,
            to_profile=to_profile,
            message=f'Пользователь {from_profile} поставил лайк на пост {post.description[:10]}!'
        )
        notification.save()
        return super().save(**kwargs)


class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ['is_view']
