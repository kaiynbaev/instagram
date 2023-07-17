from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
        ProfileViewSet, FollowersList, FollowingList,
        Unsubscribe, Subscribe
    )

router = SimpleRouter()

router.register(
    prefix=r'api/v1/profile', viewset=ProfileViewSet
)


urlpatterns = [
    path('api/v1/followers/<int:id>/', FollowersList.as_view(), name='my-followers'),
    path('api/v1/following/<int:id>/', FollowingList.as_view(), name='following'),
    path('api/v1/subscribe/<int:subscribe_account_id>/', Subscribe.as_view(), name='subscribe'),
    path('api/v1/unsubscribe/<int:unsubscribe_account_id>/', Unsubscribe.as_view(), name='unsubscribe')
] + router.urls
