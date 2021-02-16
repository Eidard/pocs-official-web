from django.contrib import admin

from board.models import Board
from board.models import Board_Category
# Register your models here.

admin.site.register(Board)
admin.site.register(Board_Category)