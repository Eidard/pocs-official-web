from django.db import models
from board.models import Board
from accounts.models import Account


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    md_content = models.TextField()
    plain_content = models.TextField(null=True)
    preview_content = models.CharField(max_length=128)
    background_image_url = models.URLField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    board_id = models.ForeignKey(Board, on_delete=models.PROTECT)
    author_id = models.ForeignKey(Account, on_delete=models.PROTECT)
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} - ' + str(self.created_at)[:10]

    class Meta:
        db_table = 'post'
        ordering = ['modified_at', 'hits', 'created_at', 'title']


class Post_Tag(models.Model):
    name = models.CharField(max_length=64)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_tag'
        ordering = ['post_id']


class Post_Recommender(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Account, on_delete=models.PROTECT)

    class Meta:
        db_table = 'post_recommender'
        ordering = ['post_id', 'author_id']

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
