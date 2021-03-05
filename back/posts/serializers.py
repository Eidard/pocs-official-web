from rest_framework import serializers
from .models import Post #, Post_Tag
from taggit import tag

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

#class PostTagSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = tags
#        fields = '__all__'
