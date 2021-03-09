import json

from django.views import View
from django.http import JsonResponse

from board.models import Board
from board.serializers import BoardSerializer, BoardCategorySerializer

from posts.models import Post
from posts.serializers import PostSerializerInIndex

from accounts.serializers import AccountSerializerInPost


class IndexView(View):
    def get(self, request):
        boards = Board.objects.all()
        response_data = []
        for board in boards:
            board_data = BoardSerializer(board).data
            board_data['category'] = BoardCategorySerializer(board.board_category).data
            posts_data = []
            posts = Post.objects.filter(board_id=board.id)[:5]
            for post in posts:
                post_data = PostSerializerInIndex(post).data
                author_data = AccountSerializerInPost(post.author_id).data
                post_data['author'] = author_data
                posts_data.append(post_data)
            board_data['posts'] = posts_data
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