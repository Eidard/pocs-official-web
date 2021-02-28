from django.urls import path, include
from .views import PostView, PostDetailView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', PostView.as_view()),
    path('<int:post_id>/', PostDetailView.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)