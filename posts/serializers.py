from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_id = serializers.ReadOnlyField(source='owner.post.id')
    post_image = serializers.ReadOnlyField(source='owner.post.image.url')
# read only and read is_owner function with get.
    is_owner = serializers.SerializerMethodField()
# implement validation checks from rest_framework validate_fieldname. 
# Automatic.
# value = loaded image

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size is bigger than 2MB'

            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image is too wide. Over 4096px'
            )
        if value.image.height >4096:
            raise serializers.ValidationError(
                'Image is too high. Over 4096px'
            )
        return value    

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content',
            'image', 'post_id', 'post_image', 'is_owner', 'image_filter',
        ]