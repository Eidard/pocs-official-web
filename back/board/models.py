from django.db import models

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    board_category = models.ForeignKey('Board_Category', on_delete=models.PROTECT)
    class Meta:
        db_table = 'board'
        ordering = ['created_at', 'name']

    def __str__(self):
        return self.name + " : " + self.board_category.name

class Board_Category(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_group', null=True, blank=True)
    class Meta:
        db_table = 'board_category'
        ordering = ['-parent__id', 'created_at', 'name']

    
    def __str__(self):
        return self.name