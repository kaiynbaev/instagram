from django.db import models
from user_profile.models import Profile

# Create your models here.
class Post(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Профиль'
    )
    image = models.ImageField(
        upload_to="posts/%Y/%m/%d",
        verbose_name='Фото'
    )
    description = models.CharField(
        max_length=500,
        verbose_name='Описание'
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )
    
    def __str__(self):
        return f"{self.profile}"
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    
class Like(models.Model):
    author = models.ForeignKey(
            Profile, 
            on_delete=models.CASCADE,
            related_name='likes',
            verbose_name='Профиль'
        )
    post = models.ForeignKey(
            Post, 
            on_delete=models.CASCADE, 
            related_name="likes",
            verbose_name='Пост'
        )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Лайк от {self.author} на {self.post}"
    
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(models.Model):
    author = models.ForeignKey(
            Profile, 
            on_delete=models.CASCADE,
            related_name='comments',
            verbose_name='Профиль'
        )
    post = models.ForeignKey(
            Post, 
            on_delete=models.CASCADE, 
            related_name="comments",
            verbose_name='Пост'
        )
    message = models.CharField(
        max_length=1000,
        verbose_name='Коментарий'
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.message}"
    
    
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        