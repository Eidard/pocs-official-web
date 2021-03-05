from django.contrib import admin

from .models import Post

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modified_at', 'tag_list')
    list_filter = ('modified_at',)
    search_fields = ('title', 'plain_content')
    #prepopulated_fields = ('title', 'preview_content', )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all()) 