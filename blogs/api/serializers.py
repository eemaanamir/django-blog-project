from django.urls import reverse
from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField
from blogs.models import Blog


class BlogListSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='blog-api:detail',
        lookup_field='pk'
    )
    user_detail_url = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'user',
            'user_detail_url',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_date_time',
            'detail_url'
        ]

    def get_user(self, obj):
        return str(obj.user.first_name) + " " + str(obj.user.last_name)

    def get_user_detail_url(self, obj):
        user_instance = obj.user
        if user_instance:
            return self.context['request'].build_absolute_uri(
                reverse('users-api:profile', args=[user_instance.pk])
            )
        return None


class BlogDetailSerializer(ModelSerializer):
    user_detail_url = SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'user',
            'user_detail_url',
            'id',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_content',
            'blog_date_time',
            'blog_likes_count',
            'blog_header_image'
        ]

    def get_user_detail_url(self, obj):
        user_instance = obj.user
        if user_instance:
            return self.context['request'].build_absolute_uri(
                reverse('users-api:profile', args=[user_instance.pk])
            )
        return None


class BlogDraftListSerializer(ModelSerializer):
    edit_url = HyperlinkedIdentityField(
        view_name='blog-api:edit',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='blog-api:delete',
        lookup_field='pk'
    )
    user = SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'user',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_date_time',
            'edit_url',
            'delete_url'
        ]

    def get_user(self, obj):
        return str(obj.user.first_name) + " " + str(obj.user.last_name)


class BlogPublishedListSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='blog-api:detail',
        lookup_field='pk'
    )
    edit_url = HyperlinkedIdentityField(
        view_name='blog-api:edit',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='blog-api:delete',
        lookup_field='pk'
    )
    user = SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'user',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_date_time',
            'detail_url',
            'edit_url',
            'delete_url'
        ]

    def get_user(self, obj):
        return str(obj.user.first_name) + " " + str(obj.user.last_name)


class BlogDraftCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_content',
            'is_published',
        ]
