"""
博客应用的过滤器类
提供文章、评论、分类和标签的过滤功能
"""

from django_filters import rest_framework as filters
from .models import Post, Comment, Category, Tag

class PostFilter(filters.FilterSet):
    """
    文章过滤器
    支持按以下字段过滤：
    - 标题（模糊匹配）
    - 内容（模糊匹配）
    - 分类（精确匹配）
    - 标签（精确匹配）
    - 状态（精确匹配）
    - 创建时间范围
    """
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    category = filters.NumberFilter(field_name='category__id')
    tags = filters.NumberFilter(field_name='tags__id')
    status = filters.ChoiceFilter(choices=Post.STATUS_CHOICES)
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'status', 'author']

class CommentFilter(filters.FilterSet):
    """
    评论过滤器
    支持按以下字段过滤：
    - 内容（模糊匹配）
    - 状态（精确匹配）
    - 所属文章（精确匹配）
    - 创建时间范围
    """
    content = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=Comment.STATUS_CHOICES)
    post = filters.NumberFilter(field_name='post__id')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Comment
        fields = ['content', 'status', 'post', 'name', 'email']

class CategoryFilter(filters.FilterSet):
    """
    分类过滤器
    支持按以下字段过滤：
    - 名称（模糊匹配）
    - 描述（模糊匹配）
    """
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name', 'description']

class TagFilter(filters.FilterSet):
    """
    标签过滤器
    支持按以下字段过滤：
    - 名称（模糊匹配）
    """
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name'] 