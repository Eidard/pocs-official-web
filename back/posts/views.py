import json
from io import StringIO
from django.shortcuts import get_object_or_404
from .models import Post #, Post_Tag
from board.models import Board
from accounts.models import Account
from markdown import Markdown, markdown
from django.http import JsonResponse
from django.views import View
from .serializers import PostSerializer

# markdown to plain text
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False

def unmark(text):
    return __md.convert(text)


class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        html_text = markdown(data['md_content'])
        plain_text = unmark(data['md_content'])

        post = Post.objects.create(
            title = data['title'],
            content = html_text,
            md_content = data['md_content'],
            plain_content =  plain_text,
            preview_content = plain_text[:128],
            background_image_url = data['background_image_url'],
            board_id = Board.objects.get(id=data['board_id']),
            author_id = Account.objects.get(id=data['author_id']),
            hits = 0
        )
        
        #post.tags.add(tag.strip() for tag in data['tags'].split(','))

        return JsonResponse({"message":"Post를 생성했습니다"}, status=200)

    def get(self, request):
        post = Post.objects.values()
        #post_tag = ', '.join(o.name for o in Post.tags.all()) 
        #print(post_tag)
        return JsonResponse({"list": list(post) + list(post_tag)}, status=200)


class PostDetailView(View):
    def post(self, request, post_id):
        data = json.loads(request.body)

        post = get_object_or_404(Post, id=post_id)

        html_text = markdown(data['md_content'])
        plain_text = unmark(data['md_content'])

        post.title = data['title']
        post.content = html_text
        post.md_content = data['md_content']
        post.plain_content =  plain_text
        post.preview_content = plain_text[:128]
        post.background_image_url = data['background_image_url']
        post.save()

        return JsonResponse({"message":"Post를 수정했습니다"}, status=200)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.hits += 1
        post.save(update_fields=['hits'])
        serializer = PostSerializer(post)
        response_data = serializer.data
        del response_data['md_content'], response_data['plain_content'], response_data['preview_content']
        
        return JsonResponse(response_data, status=200)