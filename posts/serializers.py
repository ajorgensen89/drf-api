from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_id = serializers.ReadOnlyField(source='owner.post.id')
    post_image = serializers.ReadOnlyField(source='owner.post.image.url')
# read only and read is_owner function with get.
    is_owner = serializers.SerializerMethodField()
# implement validation checks from rest_framework validate_fieldname.
# Automatic.
# value = loaded image
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size is bigger than 2MB'

            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image is too wide. Over 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image is too high. Over 4096px'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content',
            'image', 'post_id', 'post_image', 'is_owner', 'image_filter',
            'like_id', 'likes_count', 'comments_count',
        ]
