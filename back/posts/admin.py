from django.contrib import admin

from .models import Post, Post_Tag, Post_Recommender

admin.site.register(Post)
admin.site.register(Post_Tag)
admin.site.register(Post_Recommender)