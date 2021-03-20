from django.urls import path
from .views import SearchView, AuthorSearchView, TagSearchView

urlpatterns = [
    path('<str:keyword>/', SearchView.as_view()),
    path('author/<str:name>/', AuthorSearchView.as_view()),
    path('tags/<str:tag>/', TagSearchView.as_view()),
]