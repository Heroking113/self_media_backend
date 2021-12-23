"""cb_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

# 可转债小程序路由

urlpatterns = [
    path('admin_super_server/', admin.site.urls),
    path('user/', include('apps.user_manage.urls')),
    path('bc/', include('apps.base_convert.urls')),
    path('bm/', include('apps.bond_manage.urls')),
    path('cm/', include('apps.common_manage.urls')),
    path('chat/', include('apps.chat.urls'))
]

# 高校小程序路由
urlpatterns += [
    path('sch/idle/', include('apps.idle_manage.urls')),
    path('sch/topic/', include('apps.topic_manage.urls')),
    path('sch/file/', include('apps.file_manage.urls'))
]


# 开发环境下，通过此配置可获取后台的静态文件；生产环境下用nginx获取静态文件
if settings.ENV == 'DEV':
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]

