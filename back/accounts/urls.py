from django.urls import path
from accounts.views import RegisterView, LoginView, PermissionView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', RegisterView.as_view()),
    path('sessions/', LoginView.as_view()),
    path('permission/<int:user_id>/', PermissionView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)