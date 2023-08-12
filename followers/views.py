from django.shortcuts import render
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer

#     """
#     List all followers, i.e. all instances of a user
#     following another user'.
#     Create a follower, i.e. follow a user if logged in.
#     Perform_create: associate the current logged in user with a follower.
#     """


class FollowerList(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#     """
#     Retrieve a follower
#     No Update view, as we either follow or unfollow users
#     Destroy a follower, i.e. unfollow someone if owner
#     """


class FollowerDetail(generics.RetrieveDestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
