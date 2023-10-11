"""
Module: blogs.api.tests.test_views
Description: This module contains test cases for the views and functionality of the Blog API app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from blogs.models import Blog


class BlogTimeLineListAPIViewTest(TestCase):
    """
    Test case for the BlogTimeLineListAPIView.

    This test case includes tests for retrieving a timeline list of blog posts.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.blog = Blog.objects.create(
            user=self.user,
            blog_title='Test Blog',
            blog_summary='Test summary',
            blog_content='Test content',
            is_published=True
        )
        self.url = reverse('blog-api:list')

    def get_jwt_token(self):
        """
         Get a JWT token for authentication.
         """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_retrieve_blog_timeline_with_jwt(self):
        """
        Test retrieving the blog timeline with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['blog_title'], 'Test Blog')

    def test_retrieve_blog_timeline_without_jwt(self):
        """
        Test retrieving the blog timeline without a JWT token (unauthenticated).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogDetailAPIViewTest(TestCase):
    """
    Test case for the BlogDetailAPIView.

    This test case includes tests for retrieving detailed information about a blog post.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.blog = Blog.objects.create(
            user=self.user,
            blog_title='Test Blog',
            blog_summary='Test summary',
            blog_content='Test content',
            is_published=True
        )

        self.url = reverse('blog-api:detail', args=[self.blog.id])

    def get_jwt_token(self):
        """
        Get a JWT token for authentication.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_retrieve_blog_detail_with_jwt(self):
        """
        Test retrieving a blog detail with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['blog_title'], 'Test Blog')

    def test_retrieve_blog_detail_without_jwt(self):
        """
        Test retrieving a blog detail without a JWT token (unauthenticated).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogDraftListAPIViewTest(TestCase):
    """
    Test case for the BlogDraftListAPIView.

    This test case includes tests for retrieving a list of draft blog posts.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.blog_draft = Blog.objects.create(
            user=self.user,
            blog_title='Draft Blog',
            blog_summary='Draft summary',
            blog_content='Draft content',
            is_published=False
        )
        self.url = reverse('blog-api:drafts')

    def get_jwt_token(self):
        """
        Get a JWT token for authentication.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_retrieve_draft_list_with_jwt(self):
        """
        Test retrieving the draft list with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['blog_title'], 'Draft Blog')

    def test_retrieve_draft_list_without_jwt(self):
        """
        Test retrieving the draft list without a JWT token (unauthenticated).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogDraftCreateAPIViewTest(TestCase):
    """
    Test case for the BlogDraftCreateAPIView.

    This test case includes tests for creating draft blog posts.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.url = reverse('blog-api:create')

    def get_jwt_token(self):
        """
        Get a JWT token for authentication.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_create_draft_with_jwt(self):
        """
        Test creating a draft with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'blog_title': 'Test Title',
            'blog_type': 'Technology',
            'blog_topic': 'Programming',
            'blog_summary': 'This is a test summary.',
            'blog_content': 'This is the test content of the blog.',
            'is_published': False
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['blog_title'], 'Test Title')

    def test_create_draft_without_jwt(self):
        """
        Test creating a draft without a JWT token (unauthenticated).
        """
        data = {
            'blog_title': 'New Draft Blog',
            'blog_summary': 'New draft summary',
            'blog_content': 'New draft content',
            'is_published': False
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogDraftUpdateAPIViewTest(TestCase):
    """
    Test case for the BlogDraftUpdateAPIView.

    This test case includes tests for updating draft blog posts.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.blog_draft = Blog.objects.create(
            user=self.user,
            blog_title='Draft Blog',
            blog_summary='Draft summary',
            blog_content='Draft content',
            is_published=False
        )
        self.url = reverse('blog-api:edit', args=[self.blog_draft.id])

    def get_jwt_token(self):
        """
        Get a JWT token for authentication.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_update_draft_with_jwt(self):
        """
        Test updating a draft with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'blog_title': 'Updated Draft Blog',
            'blog_summary': 'Updated draft summary',
            'blog_content': 'Updated draft content',
            'is_published': False
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['blog_title'], 'Updated Draft Blog')

    def test_update_draft_without_jwt(self):
        """
        Test updating a draft without a JWT token (unauthenticated).
        """
        data = {
            'blog_title': 'Updated Draft Blog',
            'blog_summary': 'Updated draft summary',
            'blog_content': 'Updated draft content',
            'is_published': False
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogDraftDeleteAPIViewTest(TestCase):
    """
    Test case for the BlogDraftDeleteAPIView.

    This test case includes tests for deleting draft blog posts.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.blog_draft = Blog.objects.create(
            user=self.user,
            blog_title='Draft Blog',
            blog_summary='Draft summary',
            blog_content='Draft content',
            is_published=False
        )
        self.url = reverse('blog-api:delete', args=[self.blog_draft.id])

    def get_jwt_token(self):
        """
        Get a JWT token for authentication.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_delete_draft_with_jwt(self):
        """
        Test deleting a draft with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_draft_without_jwt(self):
        """
        Test deleting a draft without a JWT token (unauthenticated).
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogPublishedListAPIViewTest(TestCase):
    """
    Test case for the BlogPublishedListAPIView.

    This test case includes tests for retrieving a list of published blog posts.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.blog_published = Blog.objects.create(
            user=self.user,
            blog_title='Published Blog',
            blog_summary='Published summary',
            blog_content='Published content',
            is_published=True
        )
        self.url = reverse('blog-api:published')

    def get_jwt_token(self):
        """
        Get a JWT token for authentication.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_retrieve_published_list_with_jwt(self):
        """
        Test retrieving the published list with a valid JWT token.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['blog_title'], 'Published Blog')

    def test_retrieve_published_list_without_jwt(self):
        """
        Test retrieving the published list without a JWT token (unauthenticated).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
