from django.contrib import admin

from board.models import Board
from board.models import Board_Category
# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'board_category', 'created_at')


class Board_CategoryInline(admin.TabularInline):
    model = Board_Category


class Board_CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')

    inlines = [
        Board_CategoryInline,
    ]


admin.site.register(Board, BoardAdmin)
admin.site.register(Board_Category, Board_CategoryAdmin)