from django.urls import path
from accounts.views import UserRegisterView, LoginView, LogoutView, PermissionView, UserDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', UserRegisterView.as_view()),
    path('<int:account_id>/', UserDetailView.as_view()),
    path('sessions/', LoginView.as_view()),
    path('sessions/out/', LogoutView.as_view()),
    path('permission/<int:account_id>/', PermissionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)