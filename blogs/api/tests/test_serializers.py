"""
Module: blogs.api.tests.test_serializers
Description: This module contains test cases for the serializers in the Blogs API app.
"""
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from blogs.api.serializers import BlogDraftCreateUpdateSerializer


class BlogDraftCreateUpdateSerializerTest(TestCase):
    """
    Test case for the BlogDraftCreateUpdateSerializer.

    This test case includes tests for validating the BlogDraftCreateUpdateSerializer
    used for creating and updating draft blog posts.
    """
    def test_valid_serializer(self):
        """
        Test the serializer with valid data.
        """
        data = {
            'blog_title': 'Test Title',
            'blog_type': 'Technology',
            'blog_topic': 'Programming',
            'blog_summary': 'This is a test summary.',
            'blog_content': 'This is the test content of the blog.',
            'is_published': False
        }
        serializer = BlogDraftCreateUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_fields(self):
        """
        Test the serializer with missing required fields.
        """
        data = {
            'blog_title': '',
            'blog_type': '',
            'blog_topic': '',
            'blog_summary': '',
            'blog_content': '',
            'is_published': False
        }
        serializer = BlogDraftCreateUpdateSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(context.exception.detail['blog_title'][0],
                         'This field may not be blank.')
        self.assertEqual(context.exception.detail['blog_type'][0],
                         'This field may not be blank.')
        self.assertEqual(context.exception.detail['blog_topic'][0],
                         'This field may not be blank.')
        self.assertEqual(context.exception.detail['blog_summary'][0],
                         'This field may not be blank.')
        self.assertEqual(context.exception.detail['blog_content'][0],
                         'This field may not be blank.')

    def test_field_length_limit_exceeded(self):
        """
        Test the serializer with field length limit exceeded.
        """
        data = {
            'blog_title': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'blog_type': 'Technology',
            'blog_topic': 'Programming',
            'blog_summary': 'This is a test summary.',
            'blog_content': 'This is the test content of the blog.',
            'is_published': False
        }
        serializer = BlogDraftCreateUpdateSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(context.exception.detail['blog_title'][0],
                         'Ensure this value has at most 150 characters (it has 204).')
