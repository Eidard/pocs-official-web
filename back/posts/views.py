import os

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.conf import settings

from .markdown import *
from .common import hash_from_file, remove_saved_files_and_empty_dirs

from accounts.models import Account
from accounts.serializers import AccountSerializerInPost

from .models import Post, PostFile
from .serializers import PostDetailSerializer, PostFileDetailSerializerForNonAnonymousUser

from board.models import Board
from board.serializers import BoardCategorySerializer


class PostView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request):
        data = request.POST

        if data is None:
            return JsonResponse({"message": "잘못된 요청입니다. 다시 시도해주세요."}, status=400)

        if not request.user.is_active:
            return JsonResponse({"message":"글 생성 권한이 없습니다. 인증된 회원 계정으로 로그인 후 다시 시도해주세요."}, status=403)

        html_text = markdown(data['md_content'])
        plain_text = unmark(data['md_content'])

        background_image = settings.DEFAULT_IMAGE_RELATIVE_PATH if 'background_image_url' in data else request.FILES['background_image_url']

        savedFilePaths = []
        try:
            with transaction.atomic():
                post = Post.objects.create(
                    title = data['title'],
                    content = html_text,
                    md_content = data['md_content'],
                    plain_content =  plain_text,
                    preview_content = plain_text[:128],
                    background_image_url = background_image,
                    board_id = get_object_or_404(Board, id=data['board_id']),
                    author_id = get_object_or_404(Account, user_id=request.user.id),
                    hits = 0
                )
                savedFilePaths.append(post.background_image_real_relative_path)
                
                for f in request.FILES.getlist('files'):
                    ff = f.open()
                    file_hash = hash_from_file(ff)
                    file = PostFile.objects.create(
                        post_id = post,
                        title = f.name,
                        file = f,
                        hash = file_hash
                    )
                    ff.close()
                    savedFilePaths.append(file.file.url[1:])

                for tag in data['tags'].split(','):
                    post.tags.add(tag.strip())
        except:
            remove_saved_files_and_empty_dirs(savedFilePaths)
            return JsonResponse({"message":"글 생성에 실패했습니다. 확인 후 다시 시도해주세요."}, status=406)
        return JsonResponse({"message":"글 생성에 성공했습니다."}, status=200)

    def get(self, request):
        post = Post.objects.values()
        # post_tag = ', '.join(o.name for o in Post.tags.all())
        # print(post_tag)
        postfile = PostFile.objects.values()
        return JsonResponse({"list": list(post), "files": list(postfile)}, status=200)


class PostDetailView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request, post_id):
        data = request.POST

        if data is None:
            return JsonResponse({"message": "잘못된 요청입니다. 다시 시도해주세요."}, status=400)
        
        post = get_object_or_404(Post, id=post_id)

        if post.author_id.id != request.user.id and not request.user.is_superuser:
            return JsonResponse({"message":"해당 글 수정 권한이 없습니다. 작성자나 관리자 계정으로 로그인 후 다시 요청해주세요."}, status=401)

        html_text = markdown(data['md_content'])
        plain_text = unmark(data['md_content'])

        before_post_title = post.title

        post.title = data['title']
        post.content = html_text
        post.md_content = data['md_content']
        post.plain_content =  plain_text
        post.preview_content = plain_text[:128]
        post.board_id = get_object_or_404(Board, id=data['board_id'])

        removeFilePaths = []
        removeFilePaths.append(post.background_image_real_relative_path)        
        post.background_image_url = settings.DEFAULT_IMAGE_RELATIVE_PATH if 'background_image_url' in data else request.FILES['background_image_url']
        
        post.save()

        savedFilePaths = []
        try:
            with transaction.atomic():
                files = PostFile.objects.filter(post_id=post_id)
                fileList = list(files)
                for f in request.FILES.getlist('files'):
                    isItSameFile = False
                    try:
                        ff = f.open()
                        file_hash = hash_from_file(ff)
                        for file in files:
                            if file.hash == file_hash:
                                isItSameFile = True
                                fileList.remove(file)
                                ff.close()
                                break
                        if isItSameFile:
                            continue
                        fileInstance = PostFile.objects.create(
                                post_id = post,
                                title = f.name,
                                file = f,
                                hash = file_hash
                        )
                        savedFilePaths.append(fileInstance.file.url[1:])
                    finally:
                        ff.close()

                for file in fileList:
                    removeFilePaths.append(file.file.url[1:])
                    file.delete()
                remove_saved_files_and_empty_dirs(removeFilePaths)
                
                post.tags.clear()
                for tag in data['tags'].split(','):
                    post.tags.add(tag.strip())
        except:
            remove_saved_files_and_empty_dirs(savedFilePaths)
            return JsonResponse({"message" : f"'{before_post_title}' 글을 수정하는데 실패했습니다. 확인 후 다시 시도해주세요."}, status=406)
        return JsonResponse({"message":f"{before_post_title} 글을 수정했습니다"}, status=200)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        response_data = PostDetailSerializer(post).data

        try:
            with transaction.atomic():
                if request.user.is_active:
                    fileInstances = PostFile.objects.filter(post_id=post_id)
                    files = [PostFileDetailSerializerForNonAnonymousUser(file).data for file in fileInstances]
                else:
                    fileInstances = PostFile.objects.filter(post_id=post_id).values('title')
                    files = list(fileInstances)

                tags = [x.name for x in post.tags.all()]
        except:
            return JsonResponse({"message":"데이터를 불러오는데 실패했습니다. 다시 시도해주세요."}, status=406)

        response_data['tags'] = tags
        response_data['files'] = files
        response_data['author'] = AccountSerializerInPost(post.author_id).data
        response_data['board'] = BoardCategorySerializer(post.board_id).data
        
        post.hits += 1
        post.save(update_fields=['hits'])

        return JsonResponse(response_data, status=200)

    @method_decorator(login_required, name="dispatch")
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        if post.author_id.id != request.user.id and not request.user.is_superuser:
            return JsonResponse({"message" : "해당 글 삭제 권한이 없습니다. 작성자나 관리자 계정으로 로그인 후 다시 시도해주세요."}, status=403)

        try:
            with transaction.atomic():
                savedFilePaths = []
                savedFilePaths.append(post.background_image_real_relative_path)
                
                postFiles = PostFile.objects.filter(post_id=post_id)
                for file in postFiles:
                    savedFilePaths.append(file.file.url[1:])
                
                remove_saved_files_and_empty_dirs(savedFilePaths)
                post.tags.clear()
                post.delete()
        except:
            return JsonResponse({"message" : f"'{post.title}' 글을 삭제하는데 실패했습니다. 다시 시도해주세요."}, status=406)
        return JsonResponse({"message" : f"'{post.title}' 글이 정상적으로 삭제되었습니다"}, status=200)


class PostFileDownloadView(View):
    @method_decorator(login_required, name="dispatch")
    def get(self, request, post_id, file_name):
        if not request.user.is_active:
            return JsonResponse({"message" : "파일 다운로드 권한이 없습니다. 인증된 회원 계정으로 로그인 후 다시 시도해주세요."}, status=403)

        postFiles = PostFile.objects.filter(post_id=post_id)
        for fp in postFiles:
            if fp.real_file_name == file_name:
                filePath = fp.file.path
                if os.path.exists(filePath):
                    try:
                        with open(filePath, 'rb') as f:
                            response = HttpResponse(f.read(), content_type="application/force-download")
                            response['Content-Disposition'] = f'inline; filename={fp.title}'
                            return response
                    except:
                        return JsonResponse({"message" : "해당 파일이 존재하지 않습니다. 확인 후 다시 시도해주세요."}, status=404)