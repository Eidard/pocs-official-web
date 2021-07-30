import os
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.conf import settings

from .common import get_file_hash, remove_saved_files_and_empty_dirs, unmarkdown, trans_markdown_to_html_and_bleach
from .forms import PostFormExceptFiles
from .validators import FileValidator

from accounts.models import Account
from accounts.serializers import AccountSerializerInPost

from .models import Post, PostFile
from .serializers import PostDetailSerializer, PostFileDetailSerializerForNonAnonymousUser

from board.models import Board
from board.serializers import BoardCategorySerializer


class PostCreateView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request):        
        success_message = "글 생성에 성공했습니다."
        error_messages = {
            'wrong_request' : "잘못된 요청입니다. 다시 시도해주세요.",
            'not_permitted' : "글 생성 권한이 없습니다. 인증된 회원 계정으로 로그인 후 다시 시도해주세요.",
            'file_max_size_over' : f"첨부한 파일(들)의 총 용량이 글 하나당 저장 가능한 최대 용량({settings.MAX_FILE_UPLOAD_SIZE_TO_UNIT_NOTATION})을 넘어갑니다.",
            'invalid_board_id' : "입력한 보드가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            'fail_create_post' : "글 생성에 실패했습니다. 확인 후 다시 시도해주세요."
        }

        data = request.POST

        if data is None:
            return JsonResponse({"message": error_messages['wrong_request']}, status=400)

        if not request.user.is_active:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        form = PostFormExceptFiles(data, request.FILES)
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)
        if not Board.objects.filter(id=form.cleaned_data['board_id']).exists():
            return JsonResponse({"message":error_messages['invalid_board_id']}, status=404)

        total_file_size = 0
        for file in request.FILES.getlist('files'):
            total_file_size += file.size
            fv = FileValidator(allowed_extensions=settings.ALLOWED_FILE_EXTENTIONS)
            try:
                if total_file_size > settings.MAX_FILE_UPLOAD_SIZE:
                    raise ValidationError(message=error_messages['file_max_size_over'])
                fv(file)
            except ValidationError as e:
                return JsonResponse({"message": e.message}, status=400)

        md_content = form.cleaned_data['md_content']
        html_text = trans_markdown_to_html_and_bleach(md_content)
        plain_text = unmarkdown(md_content)

        background_image = settings.DEFAULT_IMAGE_RELATIVE_PATH if form.cleaned_data['background_image_url'] is None else form.cleaned_data['background_image_url']

        savedFilePaths = []
        try:
            with transaction.atomic():
                post = Post.objects.create(
                    title = form.cleaned_data['title'],
                    content = html_text,
                    md_content = md_content,
                    plain_content =  plain_text,
                    preview_content = plain_text[:128],
                    background_image_url = background_image,
                    board_id = get_object_or_404(Board, id=form.cleaned_data['board_id']),
                    author_id = get_object_or_404(Account, user_id=request.user.id),
                    hits = 0
                )
                savedFilePaths.append(post.background_image_real_relative_path)
                
                for f in request.FILES.getlist('files'):
                    ff = f.open()
                    file_hash = get_file_hash(ff)
                    file = PostFile.objects.create(
                        post_id = post,
                        title = f.name,
                        file = f,
                        hash = file_hash
                    )
                    ff.close()
                    savedFilePaths.append(file.file.url[1:])

                for tag in form.cleaned_data['tags'].split(','):
                    post.tags.add(tag.strip())
        except:
            remove_saved_files_and_empty_dirs(savedFilePaths)
            return JsonResponse({"message":error_messages['fail_create_post']}, status=406)
        return JsonResponse({"message":success_message}, status=200)

    def get(self, request):
        post = Post.objects.values()
        # post_tag = ', '.join(o.name for o in Post.tags.all())
        # print(post_tag)
        postfile = PostFile.objects.values()
        return JsonResponse({"list": list(post), "files": list(postfile)}, status=200)


class PostDetailView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request, post_id):
        success_message = "%(before_post_title)s 글을 수정하는데 성공했습니다"
        error_messages = {
            'wrong_request' : "잘못된 요청입니다. 다시 시도해주세요.",
            'not_permitted' : "해당 글 수정 권한이 없습니다. 작성자나 관리자 계정으로 로그인 후 다시 요청해주세요.",
            'file_max_size_over' : f"첨부한 파일(들)의 총 용량이 글 하나당 저장 가능한 최대 용량({settings.MAX_FILE_UPLOAD_SIZE_TO_UNIT_NOTATION})을 넘어갑니다.",
            'invalid_board_id' : "입력한 보드가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            'fail_update_post' : "'%(before_post_title)s' 글을 수정하는데 실패했습니다. 확인 후 다시 시도해주세요."
        }

        data = request.POST

        if data is None:
            return JsonResponse({"message":error_messages['wrong_request']}, status=400)
        
        post = get_object_or_404(Post, id=post_id)

        if post.author_id.id != request.user.id and not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=401)

        form = PostFormExceptFiles(data, request.FILES)
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)
        if not Board.objects.filter(id=form.cleaned_data['board_id']).exists():
            return JsonResponse({"message":error_messages['invalid_board_id']}, status=404)

        print(form.cleaned_data['background_image_url'])
        print(type(form.cleaned_data['background_image_url']))

        total_file_size = 0
        for file in request.FILES.getlist('files'):
            total_file_size += file.size
            fv = FileValidator(allowed_extensions=settings.ALLOWED_FILE_EXTENTIONS)
            try:
                if total_file_size > settings.MAX_FILE_UPLOAD_SIZE:
                    raise ValidationError(message=error_messages['file_max_size_over'])
                fv(file)
            except ValidationError as e:
                return JsonResponse({"message": e.message}, status=400)

        md_content = form.cleaned_data['md_content']
        html_text = trans_markdown_to_html_and_bleach(md_content)
        plain_text = unmarkdown(md_content)

        before_post_title = post.title

        post.title = form.cleaned_data['title']
        post.content = html_text
        post.md_content = md_content
        post.plain_content =  plain_text
        post.preview_content = plain_text[:128]
        post.board_id = get_object_or_404(Board, id=form.cleaned_data['board_id'])

        removeFilePaths = []
        removeFilePaths.append(post.background_image_real_relative_path)
        post.background_image_url = settings.DEFAULT_IMAGE_RELATIVE_PATH if form.cleaned_data['background_image_url'] is None else form.cleaned_data['background_image_url']
        
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
                        file_hash = get_file_hash(ff)
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
                        if not ff.closed:
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
            return JsonResponse({"message" : error_messages['fail_update_post'] % {"before_post_title":before_post_title}}, status=406)
        return JsonResponse({"message":success_message % {"before_post_title":before_post_title}}, status=200)

    def get(self, request, post_id):
        error_messages = {
            "data_load_fail" : "데이터를 불러오는데 실패했습니다. 다시 시도해주세요."
        }

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
            return JsonResponse({"message":error_messages['data_load_fail']}, status=406)

        response_data['tags'] = tags
        response_data['files'] = files
        response_data['author'] = AccountSerializerInPost(post.author_id).data
        response_data['board'] = BoardCategorySerializer(post.board_id).data
        
        post.hits += 1
        post.save(update_fields=['hits'])

        return JsonResponse(response_data, status=200)

    @method_decorator(login_required, name="dispatch")
    def delete(self, request, post_id):
        success_message = "'%(post_title)s' 글이 정상적으로 삭제되었습니다"
        error_messages = {
            "not_permitted" : "해당 글 삭제 권한이 없습니다. 작성자나 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "delete_fail" : "'%(post_title)s' 글을 삭제하는데 실패했습니다. 다시 시도해주세요."
        }
        
        post = get_object_or_404(Post, id=post_id)
        
        if post.author_id.id != request.user.id and not request.user.is_superuser:
            return JsonResponse({"message" : error_messages['not_permitted']}, status=403)

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
            return JsonResponse({"message":error_messages['delete_fail'] % {"post_title":post.title}}, status=406)
        return JsonResponse({"message":success_message % {"post_title":post.title}}, status=200)


class PostFileDownloadView(View):
    @method_decorator(login_required, name="dispatch")
    def get(self, request, post_id, file_name):
        error_messages = {
            "not_permitted" : "파일 다운로드 권한이 없습니다. 인증된 회원 계정으로 로그인 후 다시 시도해주세요.",
            "not_exist_file_in_post" : "해당 글에 등록된 파일이 없습니다. 확인 후 다시 시도해주세요.",
            "not_exist_file_in_path" : "파일이 해당 경로에 존재하지 않습니다."
        }

        if not request.user.is_active:
            return JsonResponse({"message" : error_messages['not_permitted']}, status=403)

        postFiles = PostFile.objects.filter(post_id=post_id)
        if not postFiles:
            return JsonResponse({"message" : error_messages['not_exist_file_in_post']}, status=404)
        for pf in postFiles:
            if pf.real_file_name == file_name:
                filePath = pf.file.path
                if os.path.exists(filePath):
                    try:
                        with open(filePath, 'rb') as f:
                            response = HttpResponse(f.read(), content_type="application/force-download")
                            response['Content-Disposition'] = f'inline; filename={pf.title}'
                            return response
                    except:
                        return JsonResponse({"message" : error_messages['not_exist_file_in_path']}, status=404)