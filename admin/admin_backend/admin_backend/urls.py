"""
URL configuration for admin_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Login import Login
from .views import (
    CategoryViewSet, TagViewSet, PostViewSet,
    CommentViewSet, UserProfileViewSet, SiteSettingViewSet,
    DashboardStatsView
)

# 创建路由器
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'settings', SiteSettingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Login/', Login.urls),
    path('api/', include(router.urls)),
    path('api/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    
]

# 添加媒体文件服务
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
