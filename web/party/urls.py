"""party URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from party.api_auth.views import UpdateUserView
from party.event.views import EventViewSet
from party.post.views import PostViewSet, PostImagesViewsSet

router = DefaultRouter()
router.register('post', PostViewSet)
router.register('post_images', PostImagesViewsSet)
router.register('users', UpdateUserView)
router.register('event', EventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('party.api_auth.urls')),
    path('api/v1/', include(router.urls)),
]
