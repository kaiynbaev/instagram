from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet, MainPage

router = SimpleRouter()

router.register(
    prefix=r'post', viewset=PostViewSet
)
router.register(
    prefix=r'like', viewset=LikeViewSet
)
router.register(
    prefix=r'comment', viewset=CommentViewSet
)


urlpatterns = [
    path('', MainPage.as_view(), name='main-page')
] + router.urls
