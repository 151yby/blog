"""
URL configuration for blog_django project.

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
# blog_django/urls.py

from django.contrib import admin
from django.urls import path
from accounts.views import user_login,user_register  # 导入登录视图
from music.views import search_music,download_music

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', user_login, name='user_login'),  # 添加登录 API 路由
    path('api/register/', user_register, name='user_register'),
    path('api/search_music/', search_music, name='search_music'),
    path('api/download_music/', download_music, name='download_music'),
]