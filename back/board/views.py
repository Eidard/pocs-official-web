from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json
import bleach

from accounts.serializers import AccountSerializerInPost

from posts.serializers import PostSerializerInBoard
from posts.models import Post

from .serializers import BoardSerializer, BoardCategorySerializer
from .models import Board, Board_Category
from .forms import BoardCategoryForm, BoardForm



class BoardCreateView(View):
    # @method_decorator(login_required, name="dispatch")
    def post(self, request):
        success_message = "'%(board_name)s' 보드를 생성했습니다."
        error_messages = {
            "not_permitted" : "해당 계정은 보드 생성 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "create_board_fail" : "보드 생성에 실패했습니다. 확인 후 다시 시도해주세요.",
            "not_exist_board_category" : "요청하신 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "already_exist_board" : "해당 보드는 같은 카테고리 내에 이미 존재합니다."
        }

        data = json.loads(request.body)

        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        form = BoardForm(data)
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)
        
        board_category = Board_Category.objects.filter(id = form.cleaned_data['board_category_id'])
        if not board_category.exists():
            return JsonResponse({"message":error_messages['not_exist_board_category']}, status=404)
        
        boards_in_same_category = Board.objects.filter(board_category_id = form.cleaned_data['board_category_id'])
        if list(filter(lambda x : x.name == form.cleaned_data['name'], list(boards_in_same_category))):
            return JsonResponse({"message":error_messages['already_exist_board']}, status=400)

        name = bleach.clean(form.cleaned_data['name'])
        description = bleach.clean(form.cleaned_data['description']) if form.cleaned_data['description'] is not None else None
        try:
            board = Board.objects.create(
                name = name,
                description = description,
                board_category = board_category[0]
            )
        except:
            return JsonResponse({"message":error_messages['board']}, status=403)
        return JsonResponse({"message":success_message % {"board_name":board.name}}, status=200)


class BoardDetailView(View):
    # @method_decorator(login_required, name="dispatch")
    def post(self, request, board_id):
        success_message = "'%(board_name)s' 보드를 수정했습니다."
        error_messages = {
            "not_permitted" : "해당 계정은 보드 수정 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "update_board_fail" : "보드 수정에 실패했습니다. 확인 후 다시 시도해주세요.",
            "not_exist_board_catogory" : "요청하신 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "not_exist_board" : "수정하려는 보드가 존재하지 않습니다. 확인 후 다시 시도해주세요."
        }

        data = json.loads(request.body)

        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)
        
        board = Board.objects.filter(id=board_id)
        if not board.exists():
            return JsonResponse({"message":error_messages['not_exist_board']}, status=404)
        board = board[0]

        form = BoardForm(data)
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)
        board_category = Board_Category.objects.filter(id = form.cleaned_data['board_category_id'])
        if not board_category.exists():
            return JsonResponse({"message":error_messages['not_exist_board_catogory']}, status=404)
        before_name = board.name

        board.name = bleach.clean(form.cleaned_data['name'])
        board.description = bleach.clean(form.cleaned_data['description']) if form.cleaned_data['description'] is not None else None
        board.board_category = board_category[0]
        
        try:
            board.save()
        except:
            return JsonResponse({"message":error_messages['update_board_fail']}, status=400)
        return JsonResponse({"message":success_message % {"board_name":before_name}}, status=200)

    # @method_decorator(login_required, name="dispatch")
    def delete(self, request, board_id):
        success_message = "'%(board_name)s' 보드가 삭제되었습니다."
        error_messages = {
            "not_permitted" : "해당 계정은 보드 삭제 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "delete_board_fail" : "보드 삭제에 실패했습니다. 확인 후 다시 시도해주세요.",
            "not_exist_board" : "삭제하려는 보드가 존재하지 않습니다. 확인 후 다시 시도해주세요."
        }

        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)
        
        board = Board.objects.filter(id=board_id)
        if not board.exists():
            return JsonResponse({"message":error_messages['not_exist_board']}, status=404)
        board = board[0]
        board_name = board.name

        try:
            board.delete()
        except:
            return JsonResponse({"message":error_messages['delete_board_fail']}, status=400)
        return JsonResponse({"message":success_message % {"board_name":board_name}}, status=200)


class BoardCategoryCreateView(View):
    def post(self, request):
        success_message = "'%(board_category_name)s' 보드 카테고리를 생성했습니다."
        error_messages = {
            "not_authenticated" : "로그인이 필요한 요청입니다. 로그인 후 다시 시도해주세요.",
            "not_permitted" : "해당 계정은 보드 카테고리 생성 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "create_board_category_fail" : "보드 카테고리 생성에 실패했습니다. 확인 후 다시 시도해주세요.",
            "not_exist_parent_board_category" : "요청하신 부모 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "already_exist_board_category" : "해당 카테고리는 같은 부모 카테고리 내에 이미 존재합니다.",
            "board_category_max_level_or_cycle_exist" : "해당 카테고리가 카테고리 트리에서 생성가능한 최대 레벨(%(category_max_level)s)을 넘겼거나 카테고리 트리에 사이클이 존재합니다. 확인 후 다시 입력해주세요."
        }

        data = json.loads(request.body)

        if not request.user.is_authenticated:
            return JsonResponse({"message":error_messages['not_authenticated']}, status=401)
        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        form = BoardCategoryForm(data, initial={"parent_board_category_id":None})
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)
        parent_category_id = form.cleaned_data['parent_board_category_id']
        parent_category = Board_Category.objects.filter(id=parent_category_id)
        if parent_category_id is not None and not parent_category.exists():
            return JsonResponse({"message":error_messages['not_exist_parent_board_category']}, status=404)
        
        same_level_categories = Board_Category.objects.filter(parent_id=parent_category_id)
        if list(filter(lambda x : x.name == form.cleaned_data['name'], list(same_level_categories))):
            return JsonResponse({"message":error_messages['already_exist_board_category']}, status=400)

        max_level = settings.MAX_BOARD_CATEGORY_LEVEL
        level = 1
        categories = list(Board_Category.objects.all())
        category = parent_category[0] if parent_category_id is not None else None
        while category is not None and level <= max_level:
            category = list(filter(lambda x : x.id == category.parent_id, categories))
            category = category[0] if category else None
            level += 1
        if level > max_level:
            return JsonResponse({"message":error_messages['board_category_max_level_or_cycle_exist'] % {"category_max_level":max_level}}, status=400)

        try:
            board_category = Board_Category.objects.create(
                name = bleach.clean(form.cleaned_data['name']),
                parent = parent_category[0] if parent_category.exists() else None
            )
        except:
            return JsonResponse({"message":error_messages['create_board_category_fail']}, status=400)
        return JsonResponse({"message":success_message % {"board_category_name":board_category.name}}, status=200)
        


class BoardCategoryDetailView(View):
    # @method_decorator(login_required, name="dispatch")
    def post(self, request, board_category_id):
        success_message = "'%(board_category_name)s' 보드 카테고리를 수정했습니다."
        error_messages = {
            "not_authenticated" : "로그인이 필요한 요청입니다. 로그인 후 다시 시도해주세요.",
            "not_permitted" : "해당 계정은 보드 카테고리 수정 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "update_board_category_fail" : "보드 카테고리 수정에 실패했습니다. 확인 후 다시 시도해주세요.",
            "not_exist_board_category" : "수정할 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "not_exist_parent_board_category" : "요청하신 부모 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "already_exist_board_category" : "해당 카테고리는 같은 부모 카테고리 내에 이미 존재합니다.",
            "board_category_max_level_or_cycle_exist" : "해당 카테고리가 카테고리 트리에서 생성가능한 최대 레벨(%(category_max_level)s)을 넘겼거나 카테고리 트리에 사이클이 존재합니다. 확인 후 다시 입력해주세요."
        }

        data = json.loads(request.body)

        if not request.user.is_authenticated:
            return JsonResponse({"message":error_messages['not_authenticated']}, status=401)
        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        board_category = Board_Category.objects.filter(id=board_category_id)
        if not board_category.exists():
            return JsonResponse({"message":error_messages['not_exist_board_category']}, status=404)


        form = BoardCategoryForm(data, initial={"parent_board_category_id":None})
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)
        parent_category_id = form.cleaned_data['parent_board_category_id']
        parent_category = Board_Category.objects.filter(id=parent_category_id)
        if parent_category_id is not None and not parent_category.exists():
            return JsonResponse({"message":error_messages['not_exist_parent_board_category']}, status=404)
        
        same_level_category = Board_Category.objects.filter(parent_id=parent_category_id)
        if list(filter(lambda x : x.name == form.cleaned_data['name'], list(same_level_category))):
            return JsonResponse({"message":error_messages['already_exist_board_category']})

        before_name = board_category.name
        board_category.name = bleach.clean(form.cleaned_data['name'])
        board_category.parent = parent_category[0] if parent_category_id is not None else None

        max_level = settings.MAX_BOARD_CATEGORY_LEVEL
        level = 1
        categories = list(Board_Category.objects.all())
        category = parent_category[0] if parent_category_id is not None else None
        while category is not None and level <= max_level:
            category = list(filter(lambda x : x.id == category.parent_id, categories))
            category = category[0] if category else None
            level += 1
        if level > max_level:
            return JsonResponse({"message":error_messages['board_category_max_level_or_cycle_exist'] % {"category_max_level":max_level}}, status=400)

        try:
            board_category.save()
        except:
            return JsonResponse({"message":error_messages['update_board_category_fail']}, status=400)
        return JsonResponse({"message":success_message % {"board_category_name":before_name}}, status=200)

    # @method_decorator(login_required, name="dispatch")
    def delete(self, request, board_category_id):
        success_message = "'%(board_category_name)s' 카테고리를 삭제했습니다."
        error_messages = {
            "not_authenticated" : "로그인이 필요한 요청입니다. 로그인 후 다시 시도해주세요.",
            "not_permitted" : "해당 계정은 보드 카테고리 삭제 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "delete_board_category_fail" : "보드 카테고리 삭제에 실패했습니다. 확인 후 다시 시도해주세요.",
            "not_exist_board_category" : "삭제할 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "not_exist_parent_board_category" : "요청하신 부모 보드 카테고리가 존재하지 않습니다. 확인 후 다시 시도해주세요."
        }

        if not request.user.is_authenticated:
            return JsonResponse({"message":error_messages['not_authenticated']}, status=401)
        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        category = Board_Category.objects.filter(id=board_category_id)
        if not category.exists():
            return JsonResponse({"message":error_messages['not_exist_board_category']}, status=404)

        board_category_name = category.name
        try:
            category.delete()
        except:
            return JsonResponse({"message":error_messages['delete_board_category_fail']}, status=400)
        return JsonResponse({"message":success_message % {'board_category_name':board_category_name}}, status=200)






    # def get(self, request, board_id):
    #     board = get_object_or_404(Board, id=board_id)
    #     posts_data = []
    #     posts = Post.objects.filter(board_id=board_id)
    #     for post in posts:
    #         post_data = PostSerializerInBoard(post).data
    #         post_data['author'] = AccountSerializerInPost(post.author_id).data
    #         posts_data.append(post_data)

    #     response_data = BoardSerializer(board).data
    #     response_data['posts'] = posts_data

    #     return JsonResponse(response_data, status=200)


    # def get(self, request):
    #     boards = Board.objects.all()
    #     response_data = []
    #     for board in boards:
    #         board_data = BoardSerializer(board).data
    #         board_data['category'] = BoardCategorySerializer(board.board_category).data
    #         temp = board_data['category']
    #         parent_category_obj = board.board_category.parent
    #         while parent_category_obj is not None:
    #             parent_category = BoardCategorySerializer(parent_category_obj).data
    #             temp['parent_category'] = parent_category
    #             temp = temp['parent_category']
    #             parent_category_obj = parent_category_obj.parent
    #         response_data.append(board_data)

    #     response_data = {"boards":response_data}
    #     return JsonResponse(response_data, status=200)