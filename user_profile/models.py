from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    photo = models.ImageField(
        upload_to='user_logo/%Y/%m/%d',
        verbose_name='Фото профиля'
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения'
    )
    follows = models.ManyToManyField(
            "Profile", 
            related_name="followed_by",
            blank=True
        )
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    description = models.CharField(
        max_length=500,
        verbose_name='Заголовок'
    )
    
    def current_follows_count(self) -> int:
        return self.follows.all().count()
    
    def current_age(self) -> int:
        return relativedelta(date.today(), self.date_of_birth).years

    def __str__(self):
        return f"{self.user.username} profile"
    
    @property
    def age(self):
        return self.current_age()
    
    @property
    def following_count(self):
        return self.current_follows_count()
    
    @property
    def followers_count(self):
        return self.followed_by.all().count()
    
    
    current_age.__name__ = 'Возраст'
    current_follows_count.__name__ = 'Кол-во подписок'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    