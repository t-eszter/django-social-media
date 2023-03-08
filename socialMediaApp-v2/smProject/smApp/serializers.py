from rest_framework import serializers
from .models import Profile, Post, PostLikes, Followers
 
# Create a class
class profileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Profile
        fields = '__all__'


