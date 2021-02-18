from .serializers import AccountSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from django.http import JsonResponse
from django.views import View
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import transaction
import json

'''
class SignUpView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
'''


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        Account(
            name=data['name'],
            generation=data['generation'],
            student_id=data['student_id'],
            gender=data['gender'],
            birth=data['birth'],
            phone=data['phone'],
        )


        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({"message": "이미 존재하는 계정아이디입니다."}, status=401)
        elif User.objects.filter(email=data['email']).exists():
            return JsonResponse({"message": "이미 존재하는 이메일입니다."}, status=401)
        elif Account.objects.filter(student_id=data['student_id']).exists():
            return JsonResponse({"message": "이미 존재하는 학번입니다."}, status=401)
        else:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )
                Account.objects.create(
                    user=user,
                    name=data['name'],
                    generation=data['generation'],
                    student_id=data['student_id'],
                    gender=data['gender'],
                    birth=data['birth'],
                    phone=data['phone']
                )
            return JsonResponse({"message": "회원으로 가입되셨습니다."}, status=200)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({"list": list(user)}, status=200)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = authenticate(
            username=data['username'], password=data['password']
        )
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "로그인에 성공하셨습니다."}, status=200)
        else:
            return JsonResponse({"message": "id and pw are not correct."}, status=401)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({"list": list(user)}, status=200)
