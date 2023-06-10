from django.urls import include, path
from rest_framework import routers

app_name = "blog"

router = routers.DefaultRouter()
# router.register(r"blog", blogViewSet, basename="blog")

urlpatterns = [
    path("", include(router.urls)),
]
