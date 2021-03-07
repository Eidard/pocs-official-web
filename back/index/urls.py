from django.urls import path


urlpatterns = [
    path('', IndexView.as_view()),
]
