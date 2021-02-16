from django.db import models

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    board_category = models.ForeignKey('board_Category', on_delete=models.PROTECT)
    class Meta:
        db_table = 'board'
        ordering = ['created_at', 'name']

    def __str__(self):
        parent_name = ""
        if self.board_category.parent is None :
            parent_name = "None"
        else:
            parent_name = self.board_category.parent.name
        return self.name + " : " + parent_name

class Board_Category(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='parent_board', null=True, blank=True)
    class Meta:
        db_table = 'board_category'
        ordering = ['-parent__id', 'created_at', 'name']

    
    def __str__(self):
        return self.name