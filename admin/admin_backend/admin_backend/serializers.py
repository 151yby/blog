from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment, UserProfile, SiteSetting, PostRevision, TagRelation, Notification

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("密码不匹配")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'posts_count')

    def get_posts_count(self, obj):
        return obj.posts.count()

class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at', 'posts_count')

    def get_posts_count(self, obj):
        return obj.posts.count()

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'name', 'email', 'content', 'status', 'created_at', 'parent', 'replies')

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    category_id = serializers.IntegerField(write_only=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'content', 'category', 'category_id',
                 'tags', 'tag_ids', 'status', 'views', 'created_at', 'updated_at',
                 'published_at', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids')
        post = Post.objects.create(**validated_data)
        post.tags.set(Tag.objects.filter(id__in=tag_ids))
        return post

    def update(self, instance, validated_data):
        if 'tag_ids' in validated_data:
            tag_ids = validated_data.pop('tag_ids')
            instance.tags.set(Tag.objects.filter(id__in=tag_ids))
        return super().update(instance, validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'avatar', 'bio', 'website', 'created_at', 'updated_at')

class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'

class PostRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRevision
        fields = '__all__'

class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'level', 'order', 
                 'created_at', 'updated_at', 'children', 'posts_count')

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        serializer = CategoryWithChildrenSerializer(children, many=True)
        return serializer.data

    def get_posts_count(self, obj):
        return obj.posts.count()

class TagRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRelation
        fields = '__all__'

class TagWithRelationsSerializer(serializers.ModelSerializer):
    related_tags = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at', 'related_tags')

    def get_related_tags(self, obj):
        relations = TagRelation.objects.filter(tag=obj).select_related('related_tag')
        return [{'id': r.related_tag.id, 
                'name': r.related_tag.name, 
                'weight': r.weight} for r in relations]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__' 