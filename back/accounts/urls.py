from django.urls import path
from accounts.views import RegisterView, LoginView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', RegisterView.as_view()),
    path('sessions/', LoginView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)