from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Tag, Post, Comment, UserProfile, SiteSetting, PostRevision, TagRelation, Notification
from .serializers import (CategorySerializer, TagSerializer, PostSerializer,
                        CommentSerializer, UserProfileSerializer, SiteSettingSerializer,
                        UserSerializer, PostRevisionSerializer, CategoryWithChildrenSerializer,
                        TagWithRelationsSerializer, NotificationSerializer)
from .filters import PostFilter, CommentFilter, CategoryFilter, TagFilter
from django.core.files.storage import default_storage
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import markdown
from django.db.models import Q
from django.utils.text import slugify


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = CategoryFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        category = self.get_object()
        posts = category.posts.all()
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CategoryWithChildrenSerializer
        return CategorySerializer

    @action(detail=True, methods=['post'])
    def merge(self, request, pk=None):
        """合并两个分类"""
        category = self.get_object()
        target_category_id = request.data.get('target_category_id')
        if not target_category_id:
            return Response({'error': '目标分类ID不能为空'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        target_category = get_object_or_404(Category, id=target_category_id)
        # 更新所有文章的分类
        Post.objects.filter(category=category).update(category=target_category)
        # 更新子分类的父分类
        Category.objects.filter(parent=category).update(parent=target_category)
        category.delete()
        return Response({'status': 'success'})

    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        """调整分类顺序"""
        category = self.get_object()
        new_order = request.data.get('order')
        if new_order is None:
            return Response({'error': '新的顺序不能为空'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        category.order = new_order
        category.save()
        return Response({'status': 'success'})

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        tag = self.get_object()
        posts = tag.posts.all()
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TagWithRelationsSerializer
        return TagSerializer

    @action(detail=True, methods=['post'])
    def update_relations(self, request, pk=None):
        """更新标签关联关系"""
        tag = self.get_object()
        related_tags = request.data.get('related_tags', [])
        
        # 清除旧的关联
        TagRelation.objects.filter(tag=tag).delete()
        
        # 创建新的关联
        for related_tag_data in related_tags:
            related_tag = get_object_or_404(Tag, id=related_tag_data['id'])
            weight = related_tag_data.get('weight', 1.0)
            TagRelation.objects.create(
                tag=tag,
                related_tag=related_tag,
                weight=weight
            )
        return Response({'status': 'success'})

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """批量删除标签"""
        tag_ids = request.data.get('tag_ids', [])
        if not tag_ids:
            return Response({'error': '标签ID列表不能为空'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        Tag.objects.filter(id__in=tag_ids).delete()
        return Response({'status': 'success'})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at', 'updated_at', 'views']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(status='published')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.publish()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        post = self.get_object()
        post.views += 1
        post.save()
        return Response({'status': 'success'})

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """
        上传文章图片
        - 处理图片存储到 media/posts/images/ 目录
        - 返回上传图片的URL
        """
        post = self.get_object()
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        image = request.FILES['image']
        # Save image to media/posts/images/
        image_name = f'posts/images/{post.id}_{image.name}'
        image_path = default_storage.save(image_name, image)
        image_url = default_storage.url(image_path)
        
        return Response({'url': image_url})

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        """保存文章修改历史"""
        instance = self.get_object()
        # 创建修改历史记录
        PostRevision.objects.create(
            post=instance,
            title=instance.title,
            content=instance.content,
            created_by=self.request.user
        )
        serializer.save()

    @action(detail=False, methods=['get'])
    def drafts(self, request):
        """
        获取当前用户的所有草稿文章
        - 支持分页功能
        - 返回草稿文章列表
        """
        drafts = Post.objects.filter(author=request.user, status='draft')
        page = self.paginate_queryset(drafts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        获取所有已发布的文章
        - 支持分页功能
        - 返回已发布文章列表
        """
        published = Post.objects.filter(status='published')
        page = self.paginate_queryset(published)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(published, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        切换文章状态（草稿/已发布）
        - 更新文章状态
        - 返回更新后的文章数据
        """
        post = self.get_object()
        post.status = 'published' if post.status == 'draft' else 'draft'
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def render_markdown(self, request, pk=None):
        """渲染文章的Markdown内容"""
        post = self.get_object()
        rendered_content = markdown.markdown(
            post.content,
            extensions=['extra', 'codehilite', 'toc']
        )
        return Response({'rendered_content': rendered_content})

    @action(detail=True, methods=['get'])
    def revision_history(self, request, pk=None):
        """获取文章的修改历史"""
        post = self.get_object()
        revisions = PostRevision.objects.filter(post=post)
        serializer = PostRevisionSerializer(revisions, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilter
    search_fields = ['content', 'name', 'email']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Comment.objects.all()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(status='approved')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.status = 'approved'
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        comment = self.get_object()
        comment.status = 'rejected'
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        获取所有待审核的评论
        - 支持分页功能
        - 返回待审核评论列表
        """
        pending = Comment.objects.filter(status='pending')
        page = self.paginate_queryset(pending)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def approved(self, request):
        """
        获取所有已批准的评论
        - 支持分页功能
        - 返回已批准评论列表
        """
        approved = Comment.objects.filter(status='approved')
        page = self.paginate_queryset(approved)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(approved, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        切换评论状态（待审核/已批准）
        - 更新评论状态
        - 返回更新后的评论数据
        """
        comment = self.get_object()
        comment.status = 'approved' if comment.status == 'pending' else 'pending'
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def _check_spam(self, content):
        """检查评论是否为垃圾评论"""
        # 简单的垃圾评论检查规则
        spam_keywords = ['viagra', 'casino', 'porn', 'xxx']
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in spam_keywords)

    def _send_notification(self, comment):
        """发送评论通知"""
        # 给文章作者发送通知
        Notification.objects.create(
            user=comment.post.author,
            type='comment',
            post=comment.post,
            comment=comment,
            content=f'您的文章"{comment.post.title}"收到了新评论'
        )
        
        # 如果是回复评论，给被回复的评论作者发送通知
        if comment.parent:
            Notification.objects.create(
                user=comment.parent.user,
                type='reply',
                post=comment.post,
                comment=comment,
                content=f'您的评论收到了新回复'
            )

    def perform_create(self, serializer):
        comment = serializer.save()
        # 检查是否为垃圾评论
        if self._check_spam(comment.content):
            comment.status = 'rejected'
            comment.save()
        else:
            # 发送通知
            self._send_notification(comment)

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        """获取评论通知"""
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """标记通知为已读"""
        notification = get_object_or_404(Notification, id=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def upload_avatar(self, request, pk=None):
        """
        上传用户头像
        - 处理头像存储到 media/avatars/ 目录
        - 自动删除旧的头像文件
        - 返回更新后的用户资料数据
        """
        profile = self.get_object()
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Delete old avatar if exists
        if profile.avatar:
            default_storage.delete(profile.avatar.path)
        
        avatar = request.FILES['avatar']
        # Save avatar to media/avatars/
        avatar_name = f'avatars/{profile.user.id}_{avatar.name}'
        profile.avatar.save(avatar_name, avatar)
        
        return Response(UserProfileSerializer(profile).data)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        获取当前用户的资料
        - 返回已认证用户的资料数据
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_settings(self, request, pk=None):
        """
        更新用户资料设置
        - 支持部分字段更新
        - 返回更新后的资料数据或验证错误信息
        """
        profile = self.get_object()
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiteSettingViewSet(viewsets.ModelViewSet):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        return SiteSetting.objects.first()

# Dashboard Statistics Views
class DashboardStatsView(APIView):
    """
    仪表盘统计数据视图
    - 需要用户认证
    - 缓存5分钟
    - 提供以下统计数据：
      * 总体统计（文章、浏览量、评论数）
      * 月度统计
      * 环比增长
      * 分类统计
      * 标签统计
      * 最近30天每日浏览量
    """
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    @method_decorator(vary_on_cookie)
    def get(self, request):
        # Get current month stats
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Basic stats
        total_posts = Post.objects.count()
        total_views = Post.objects.aggregate(total_views=Sum('views'))['total_views'] or 0
        total_comments = Comment.objects.count()
        
        # Monthly stats
        monthly_posts = Post.objects.filter(created_at__gte=month_start).count()
        monthly_views = Post.objects.filter(created_at__gte=month_start).aggregate(
            monthly_views=Sum('views'))['monthly_views'] or 0
        monthly_comments = Comment.objects.filter(created_at__gte=month_start).count()
        
        # Calculate growth
        last_month_start = month_start - timezone.timedelta(days=month_start.day)
        last_month_posts = Post.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=month_start).count()
        last_month_views = Post.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=month_start).aggregate(
            last_views=Sum('views'))['last_views'] or 0
        last_month_comments = Comment.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=month_start).count()
        
        # Calculate growth percentages
        posts_growth = ((monthly_posts - last_month_posts) / (last_month_posts or 1)) * 100
        views_growth = ((monthly_views - last_month_views) / (last_month_views or 1)) * 100
        comments_growth = ((monthly_comments - last_month_comments) / (last_month_comments or 1)) * 100

        # Get category distribution
        category_stats = Category.objects.annotate(
            posts_count=Count('posts'),
            total_views=Sum('posts__views')
        ).values('name', 'posts_count', 'total_views')

        # Get tag distribution
        tag_stats = Tag.objects.annotate(
            posts_count=Count('posts'),
            total_views=Sum('posts__views')
        ).values('name', 'posts_count', 'total_views')

        # Get daily views for the last 30 days
        thirty_days_ago = now - timezone.timedelta(days=30)
        daily_views = Post.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            select={'date': 'date(created_at)'}
        ).values('date').annotate(
            total_views=Sum('views')
        ).order_by('date')
        
        return Response({
            'total_stats': {
                'posts': total_posts,
                'views': total_views,
                'comments': total_comments,
            },
            'monthly_stats': {
                'posts': monthly_posts,
                'views': monthly_views,
                'comments': monthly_comments,
            },
            'growth': {
                'posts': round(posts_growth, 1),
                'views': round(views_growth, 1),
                'comments': round(comments_growth, 1),
            },
            'category_stats': category_stats,
            'tag_stats': tag_stats,
            'daily_views': daily_views,
        }) 