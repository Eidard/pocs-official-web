import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

from .markdown import *
from .common import remove_saved_files_and_empty_dirs

from accounts.models import Account
from accounts.serializers import AccountSerializerInPost

from .models import Post, PostFile
from .serializers import PostDetailSerializer

from board.models import Board
from board.serializers import BoardCategorySerializer


class PostView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request):
        data = request.POST

        if data is None:
            return JsonResponse({"message": "잘못된 요청입니다. 다시 시도해주세요."}, status=400)

        html_text = markdown(data['md_content'])
        plain_text = unmark(data['md_content'])

        savedFilePaths = []
        try:
            with transaction.atomic():
                post = Post(
                    title = data['title'],
                    content = html_text,
                    md_content = data['md_content'],
                    plain_content =  plain_text,
                    preview_content = plain_text[:128],
                    background_image_url = request.FILES['background_image_url'],
                    board_id = Board.objects.get(id=data['board_id']),
                    author_id = Account.objects.get(user_id=request.user.id),
                    hits = 0
                )

                files = []
                for f in request.FILES.getlist('files'):
                    files.append(PostFile(
                        post_id = post,
                        title = f.name,
                        file = f
                    ))

                for tag in data['tags'].split(','):
                    post.tags.add(tag.strip())

                post.save()
                savedFilePaths.append(post.background_image_url.path[51:].replace('\\', '/'))
                for file in files:
                    file.save()
                    savedFilePaths.append(file.file.path[51:].replace('\\', '/'))
        except:
            try:
                remove_saved_files_and_empty_dirs(savedFilePaths)
            except:
                pass
            return JsonResponse({"message":"글 생성에 실패했습니다"}, status=406)
        return JsonResponse({"message":"글을 생성했습니다"}, status=200)

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

            return JsonResponse({"message":"글을 수정했습니다"}, status=200)
        else:
            return JsonResponse({"message":"해당 글 수정 권한이 없습니다"}, status=401)

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
            try:
                with transaction.atomic():
                    post.tags.clear()
                    post.delete()
            except:
                return JsonResponse({"message" : f"'{post.title}' 글을 삭제하던 중 오류가 발생했습니다."}, status=406)
            return JsonResponse({"message" : f"'{post.title}' 글이 삭제되었습니다"}, status=200)
        else:
            return JsonResponse({"message" : "해당 글 삭제 권한이 없습니다"}, status=401)