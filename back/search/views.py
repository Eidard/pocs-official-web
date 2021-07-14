import re

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from posts.models import Post
from posts.serializers import PostSerializerInBoard

from accounts.models import Account
from accounts.serializers import AccountSerializerInPost, AccountSerializerInSearch

# Create your views here.

class SearchView(View):
    def get(self, request, keyword):
        if len(keyword) < 2:
            return JsonResponse({"message":"최소 2글자 이상의 검색어를 입력해 주세요"}, status=401)

        p = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9-]+')
        m = p.match(keyword)
        if m is None or m.group() != keyword:
            return JsonResponse({"message":"잘못된 검색어를 입력했습니다. 다시 입력해주세요"}, status=401)

        query_keyword = keyword.replace('-', '" "')
        query = f'SELECT * FROM post WHERE match(post.title, post.plain_content) against("{query_keyword}");'
        searched_posts = Post.objects.raw(query)
        posts_data = []
        response_data = {}
        for post in searched_posts:
            post_data = PostSerializerInBoard(post).data
            post_data['author'] = AccountSerializerInPost(post.author_id).data
            posts_data.append(post_data)
        response_data['posts'] = posts_data
        if response_data['posts']:
            response_data['searchKeyword'] = keyword.replace('-', ' ')
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"message":f"'{keyword.replace('-', ' ')}'의 검색 결과가 없습니다"}, status=200)


class AuthorSearchView(View):
    def get(self, request, name):
        authors = Account.objects.filter(name = name)
        authors_data = []
        response_data = {}
        for author in authors:
            posts_data = []
            posts = Post.objects.filter(author_id = author.id)
            for post in posts:
                post_data = PostSerializerInBoard(post).data
                post_data['author'] = AccountSerializerInPost(post.author_id).data
                posts_data.append(post_data)
            author_data = AccountSerializerInSearch(author).data
            author_data['posts'] = posts_data
            authors_data.append(author_data)
        response_data['authors'] = authors_data
        if response_data['authors']:
            response_data['searchKeyword'] = name
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"message":f"작성자 '{name}'의 검색 결과가 없습니다"}, status=200)


class TagSearchView(View):
    def get(self, request, tag):
        posts = Post.objects.filter(tags__name__in=[tag])
        posts_data = []
        response_data = {}
        for post in posts:
            post_data = PostSerializerInBoard(post).data
            posts_data.append(post_data)
        response_data['posts'] = posts_data
        if response_data['posts']:
            response_data['searchKeyword'] = tag
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"message":f"해시태그 '{tag}'의 검색 결과가 없습니다"}, status=200)