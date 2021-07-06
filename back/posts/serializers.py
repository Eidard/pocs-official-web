from rest_framework import serializers
from .models import Post, PostFile
# from taggit import tag

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostSerializerInBoard(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'preview_content', 'background_image_url', 'created_at', 'hits')

class PostSerializerInIndex(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at')

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'background_image_url', 'created_at', 'modified_at', 'hits')
        
class PostFileDetailSerializerForNonAnonymousUser(serializers.ModelSerializer):
    real_file_name = serializers.ReadOnlyField()

    class Meta:
        model = PostFile
        fields = ('title', 'real_file_name')