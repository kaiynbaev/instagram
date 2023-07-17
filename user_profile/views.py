from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, parsers
from rest_framework.response import Response
from .serializers import (ProfileSerializers, PatchUpdateProfileSerializer, UpdateProfileSerializer)
from .models import Profile
# Create your views here.


class ProfileViewSet(ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action in 'update':
            return UpdateProfileSerializer
        elif self.action == 'partial_update':
            return PatchUpdateProfileSerializer
        print(self.action, '\n\n\n\n\n\n\n')
        return ProfileSerializers
    
    
class FollowersList(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, *args, **kwargs):
        return Response(
            status=status.HTTP_200_OK
        )
        
        
class FollowersList(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, *args, **kwargs):
        client_id = kwargs.get('id')
        if client_id is not None:
            client = get_object_or_404(Profile, id=client_id)
            data = client.follows.all().values('id', 'photo', username=F('user__username'))
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )
        
        
class FollowingList(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, *args, **kwargs):
        client_id = kwargs.get('id')
        if client_id is not None:
            client = get_object_or_404(Profile, id=client_id)
            data = client.followed_by.all().values('id', 'photo', username=F('user__username'))
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )


class Subscribe(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        # if (current_account_id := kwargs.get('current_account_id')) is not None:
        #     current_account = get_object_or_404(Profile, id=current_account_id)
        if (subscribe_account_id := kwargs.get('subscribe_account_id')) is not None:
            subscribe_account = get_object_or_404(Profile, id=subscribe_account_id)
        if (current_account := self.request.user.profile) == subscribe_account:
            return Response(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={'detail': f'{subscribe_account} не может подписаться на самого себя!'}
        )
        subscribe_account.follows.add(
            current_account
        )
        
        return Response(
            status=status.HTTP_200_OK
        )
        

class Unsubscribe(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, *args, **kwargs):
        current_account = self.request.user.profile
        if (unsubscribe_account_id := kwargs.get('unsubscribe_account_id')) is not None:
            unsubscribe_account = get_object_or_404(Profile, id=unsubscribe_account_id)
        
        accounts = current_account.followed_by.filter(id=unsubscribe_account.id).values_list('id', flat=True)
    
        for account in accounts:
            current_account.followed_by.remove(account)
            
        return Response(
            status=status.HTTP_200_OK
        )
