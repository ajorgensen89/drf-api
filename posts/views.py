from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    # Better forms.
    serializer_class = PostSerializer
    # import of permissions to check if user if logged in. IN A LIST.
    # NO FORM if not logged in.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    # list all posts and serilizer them. return serialized data in Response

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    # Check info coming it and throw error or valid status
    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )