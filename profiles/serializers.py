from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_name = serializers.ReadOnlyField(source='owner.profile.name')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
# read only and read is_owner function with get.
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'content',
            'image', 'profile_name', 'profile_image', 'is_owner',
        ]