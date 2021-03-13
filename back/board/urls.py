from django.urls import path
from board.views import BoardsView, BoardDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', BoardsView.as_view()),
    path('<int:board_id>/', BoardDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)