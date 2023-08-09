from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='ava', password='pass')

    def test_can_list_posts(self):
        ava = User.objects.get(username='ava')
        Post.objects.create(owner=ava, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='ava', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # do not need to log in or fetch anything from the database like above.
    # 200_OK for passin test.
    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class PostDetailViewTests(APITestCase):
#     def setUp(self):
#         ava = User.objects.create_user(username='ava', password='pass')
#         david = User.objects.create_user(username='david', password='pass')
#         Post.objects.create(
#             owner=ava, title='a title', content='avas content'
#         )
#         Post.objects.create(
#             owner=david, title='another title', content='davids content'
#         )

#     def test_can_retrieve_post_using_valid_id(self):
#         response = self.client.get('/posts/1/')
#         self.assertEqual(response.data['title'], 'a title')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostDetailViewTests(APITestCase):
    def setUp(self):
        ava = User.objects.create_user(username='ava', password='pass')
        david = User.objects.create_user(username='david', password='pass')
        Post.objects.create(
            owner=ava, title='a title', content='ava content'
        )
        Post.objects.create(
            owner=david, title='another title', content='davids content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    # To make it fail pass 201_CREATED code

    def test_user_can_update_own_post(self):
        self.client.login(username='ava', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # make it tail by adding a passible HTTP_200_OK.
    def test_user_cant_update_another_users_post(self):
        # force login
        self.client.login(username='ava', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
