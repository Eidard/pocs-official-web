from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostFileDownloadView, PostCreateView, PostDetailView


urlpatterns = [
    path('', PostCreateView.as_view()),
    path('<int:post_id>/', PostDetailView.as_view()),
    path('<int:post_id>/download/<str:file_name>/', PostFileDownloadView.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)