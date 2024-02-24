from rest_framework import serializers
from notification.models import Post, User
from backend.utils import build_absolute_url
from django.templatetags.static import static

# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title")

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "name", "avatar_url")
    
    def get_avatar_url(self, obj):
        # Method to generate avatar URL based on the avatar_image_name
        if obj.avatar_image_name:
            return build_absolute_url(static("portraits/{}".format(obj.avatar_image_name)))
        return None

    def to_representation(self, instance):
        # Call the parent class's to_representation method
        representation = super().to_representation(instance)

        # Override the value of a specific field
        representation['name'] = instance.name if instance.name else "User"

        return representation