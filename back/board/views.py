from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import json

from accounts.serializers import AccountSerializerInPost

from posts.serializers import PostSerializerInBoard
from posts.models import Post

from .serializers import BoardSerializer, BoardCategorySerializer
from .models import Board, Board_Category



class BoardsView(View):
    def get(self, request):
        boards = Board.objects.all()
        response_data = []
        for board in boards:
            board_data = BoardSerializer(board).data
            board_data['category'] = BoardCategorySerializer(board.board_category).data
            temp = board_data['category']
            parent_category_obj = board.board_category.parent
            while parent_category_obj is not None:
                parent_category = BoardCategorySerializer(parent_category_obj).data
                temp['parent_category'] = parent_category
                temp = temp['parent_category']
                parent_category_obj = parent_category_obj.parent
            response_data.append(board_data)

        response_data = {"boards":response_data}
        return JsonResponse(response_data, status=200)


class BoardDetailView(View):
    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        posts_data = []
        posts = Post.objects.filter(board_id=board_id)
        for post in posts:
            post_data = PostSerializerInBoard(post).data
            post_data['author'] = AccountSerializerInPost(post.author_id).data
            posts_data.append(post_data)

        response_data = BoardSerializer(board).data
        response_data['posts'] = posts_data

        return JsonResponse(response_data, status=200)
