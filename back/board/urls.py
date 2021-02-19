from django.urls import path
from board.views import BoardsView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', BoardsView.as_view()),
    # path('sessions/', LoginView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)