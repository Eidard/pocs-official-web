from django.urls import path
from .views import BoardCategoryCreateView, BoardCategoryDetailView, BoardCreateView, BoardDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', BoardCreateView.as_view()),
    path('<int:board_id>/', BoardDetailView.as_view()),
    path('category/', BoardCategoryCreateView.as_view()),
    path('category/<int:board_category_id>/', BoardCategoryDetailView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)