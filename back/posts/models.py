from django.conf import settings
from django.db import models
from board.models import Board
from accounts.models import Account
from taggit.managers import TaggableManager

from .common import file_upload_path


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()  # 유저가 입력한 마크다운 텍스트를 HTML로 렌더링시킨 상태
    md_content = models.TextField()  # 유저가 입력한 값 그대로 (마크다운형식을 따랐을 것이라고 가정)
    # 유저가 입력한 마크다운 텍스트를 일반 텍스트로 변환 (HTML로 치면 태그 제거된 텍스트)
    plain_content = models.TextField(null=True)
    preview_content = models.CharField(
        max_length=128)  # 플레인 컨텐츠 중에서 적당히 앞에 있는 128자
    background_image_url = models.ImageField(upload_to=settings.BACKGROUND_IMAGES_MEDIA_DIR, default=settings.DEFAULT_IMAGE_RELATIVE_PATH)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    board_id = models.ForeignKey(Board, on_delete=models.PROTECT)
    author_id = models.ForeignKey(Account, on_delete=models.PROTECT)
    hits = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    
    @property
    def background_image_real_relative_path(self):
        return self.background_image_url.path[len(str(settings.BASE_DIR)) + 1:].replace('\\', '/')

    def __str__(self):
        return f'{self.title} - ' + str(self.created_at)[:10]

    class Meta:
        db_table = 'post'
        ordering = ['modified_at', 'hits', 'created_at', 'title']


class PostFile(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    file = models.FileField(upload_to=file_upload_path, null=True)

    def __str__(self):
        return self.title

    @property
    def real_file_name(self):
        return self.file.name[self.file.name.rfind('/') + 1:]

    class Meta:
        db_table = 'files'
        ordering = ['post_id', 'title']


# class Comment(models.Model):
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author_id = models.ForeignKey(Account, on_delete=models.CASCADE)
#     content = models.TextField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
#     class Meta:
#         ordering = ['-created_at']

#     def children(self):
#         return Comment.objects.filter(parent_id=self)

#     def is_parent(self):
#         if self.parent_id is not None:
#             return False
#         return True
