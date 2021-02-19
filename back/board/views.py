from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import json

from .serializers import BoardSerializer
from .models import Board, Board_Category


class BoardsView(View):
    def get(self, request):
        boards = Board.objects.values()
        boards_category = Board_Category.objects.values()
        return JsonResponse({"boards": list(boards), "category" : list(boards_category)}, status=200)
