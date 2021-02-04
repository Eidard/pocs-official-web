from django.urls import path
from accounts.views import SignUpView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', SignUpView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)