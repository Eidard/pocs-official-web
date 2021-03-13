import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

from .markdown import *

from accounts.models import Account
from accounts.serializers import AccountSerializerInPost

from .models import Post
from .serializers import PostDetailSerializer

from board.models import Board
from board.serializers import BoardCategorySerializer


class PostView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request):
        data = json.loads(request.body)

        html_text = markdown(data['md_content'])
        plain_text = unmark(data['md_content'])
        
        with transaction.atomic():
            post = Post.objects.create(
                title = data['title'],
                content = html_text,
                md_content = data['md_content'],
                plain_content =  plain_text,
                preview_content = plain_text[:128],
                background_image_url = data['background_image_url'],
                board_id = Board.objects.get(id=data['board_id']),
                author_id = Account.objects.get(user_id=request.user.id),
                hits = 0
            )
            for tag in data['tags'].split(','):
                post.tags.add(tag.strip())

        return JsonResponse({"message":"Post를 생성했습니다"}, status=200)

    def get(self, request):
        post = Post.objects.values()
        # post_tag = ', '.join(o.name for o in Post.tags.all())
        # print(post_tag)
        return JsonResponse({"list": list(post)}, status=200)


class PostDetailView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request, post_id):
        data = json.loads(request.body)

        post = get_object_or_404(Post, id=post_id)

        if post.author_id.id == request.user.id or request.user.is_superuser:
            html_text = markdown(data['md_content'])
            plain_text = unmark(data['md_content'])

            post.title = data['title']
            post.content = html_text
            post.md_content = data['md_content']
            post.plain_content =  plain_text
            post.preview_content = plain_text[:128]
            post.background_image_url = data['background_image_url']

            with transaction.atomic():
                post.tags.clear()
                for tag in data['tags'].split(','):
                    post.tags.add(tag.strip())
                post.save()

            return JsonResponse({"message":"Post를 수정했습니다"}, status=200)
        else:
            return JsonResponse({"message":"Post 수정 권한이 없습니다"}, status=403)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.hits += 1
        post.save(update_fields=['hits'])
        response_data = PostDetailSerializer(post).data
        tags = []
        for tag in post.tags.all():
            tags.append(str(tag))
        response_data['tags'] = tags
        response_data['author'] = AccountSerializerInPost(post.author_id).data
        response_data['board'] = BoardCategorySerializer(post.board_id).data
        
        return JsonResponse(response_data, status=200)

    @method_decorator(login_required, name="dispatch")
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        if post.author_id.id == request.user.id or request.user.is_superuser:
            return_message = "'" + post.title + "' 글이 삭제되었습니다"
            post.tags.clear()
            post.delete()        
            return JsonResponse({"message" : return_message}, status=200)
        else:
            return JsonResponse({"message" : "Post 삭제 권한이 없습니다"}, status=200)