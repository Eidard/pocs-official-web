from django.shortcuts import render
from .models import Post
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer


