from rest_framework import serializers
from .models import Post, Post_Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Tag
        fields = '__all__'