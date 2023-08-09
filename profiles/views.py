from django.http import Http404
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        # To get many profiles
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # self and primary key as arguments.

    def get_object(self, pk):
        try:
            # Get profile by primary key
            profile = Profile.objects.get(pk=pk)
            # throw error
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            # import at the top
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        # To get one profile
        serializer = ProfileSerializer(
            profile, context={'request': request})
        # return data in a Response
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
