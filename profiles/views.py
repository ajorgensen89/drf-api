from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

# from django.http import Http404
# from rest_framework import status
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Profile
# from .serializers import ProfileSerializer
# from drf_api.permissions import IsOwnerOrReadOnly

# class ProfileList(APIView):
#     def get(self, request):
#         profiles = Profile.objects.all()
#         # To get many profiles
#         serializer = ProfileSerializer(
#             profiles, many=True, context={'request': request})
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsOwnerOrReadOnly]
#     # self and primary key as arguments.

#     def get_object(self, pk):
#         try:
#             # Get profile by primary key
#             profile = Profile.objects.get(pk=pk)
#             # throw error
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             # import at the top
#             raise Http404

#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         # To get one profile
#         serializer = ProfileSerializer(
#             profile, context={'request': request})
#         # return data in a Response
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.
#         HTTP_400_BAD_REQUEST)


# class ProfileList(generics.ListAPIView):
#     """
#     List all profiles.
#     No create view as profile creation is handled by django signals.
#     """
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


# class ProfileDetail(generics.RetrieveUpdateAPIView):
#     """
#     Retrieve or update a profile if you're the owner.
#     """
#     permission_classes = [IsOwnerOrReadOnly]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
