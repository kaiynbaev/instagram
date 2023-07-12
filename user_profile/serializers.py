from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        ref_name = "User t"
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileShortViewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Profile
        fields = ['user', 'photo']


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    age = serializers.SerializerMethodField(
        read_only=True
    )
    followers = serializers.SerializerMethodField(
        read_only=True
    )
    following = serializers.SerializerMethodField(
        read_only=True
    )
    
    # follows= ProfileShortViewSerializer(
    #     many=True, read_only=True
    # )
    # followed_by = ProfileShortViewSerializer(
    #         many=True, read_only=True
    #     )
    
    def get_followers(self, obj):
       return getattr(obj, 'followers_count')
   
    def get_following(self, obj):
       return getattr(obj, 'following_count')
    
    def get_age(self, obj):
       return getattr(obj, 'age')
    
    class Meta:
        model = Profile
        ref_name = "Profile"
        fields = ["id", "user", "age", "photo", "title",
                  "description", "followers", "following"]



class UpdateProfileSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Profile
        fields = [
            "date_of_birth", "photo", "title",
            "description"
        ]

class PatchUpdateProfileSerializer(UpdateProfileSerializer):
    
    photo = serializers.FileField(
        required=False
    )
    date_of_birth = serializers.DateField(
        required=False
    )
    title = serializers.CharField(
        required=False
    )
    description = serializers.CharField(
        required=False
    )
