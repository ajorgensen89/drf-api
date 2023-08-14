from django.db.models import Count
from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        # user feed
        'owner__followed__owner__profile',
        # user liked posts
        'likes__owner__profile',
        # user posts
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')

# from django.shortcuts import render
# from rest_framework import status, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Post
# from .serializers import PostSerializer
# from django.http import Http404
# from drf_api.permissions import IsOwnerOrReadOnly


# class PostList(APIView):
#     # Better forms.
#     serializer_class = PostSerializer
#     # import of permissions to check if user if logged in. IN A LIST.
#     # NO FORM if not logged in. Need from import.
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly
#     ]

#     # list all posts and serilizer them. return serialized data in Response

#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts, many=True, context={'request': request}
#         )
#         return Response(serializer.data)

#     # Check info coming it and throw error or valid status
#     def post(self, request):
#         serializer = PostSerializer(
#             data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(
#                 serializer.data, status=status.HTTP_201_CREATED
#             )
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#         )


# class PostDetail(APIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     serializer_class = PostSerializer

#     # get posts

#     def get_object(self, pk):
#         try:
#             post = Post.objects.get(pk=pk)
#             self.check_object_permissions(self.request, post)
#             return post
#         except Post.DoesNotExist:
#             # Need from import
#             raise Http404

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(
#             post, context={'request': request}
#         )
#         return Response(serializer.data)

#     # update posts

#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(
#             post, data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#         )

#     # delete post

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )
