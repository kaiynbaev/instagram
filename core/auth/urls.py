from django.urls import path
from .views import ActivateUser

urlpatterns = [
    path('accounts/activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
]
