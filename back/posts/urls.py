from django.urls import path, include
from .views import PostsViewSet
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)