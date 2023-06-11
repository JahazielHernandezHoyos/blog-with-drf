from django.urls import path, include
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.AccountAuthViewSet)
router.register(r'register', viewsets.AccountRegisterViewSet)
router.register(r'comments', viewsets.CommentsViewSet)
router.register(r'entrances', viewsets.EntranceViewSet)
router.register(r'categories', viewsets.CategoryViewSet)
router.register(r'tags', viewsets.TagsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
