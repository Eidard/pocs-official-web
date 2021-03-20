import json
import re
import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import transaction

from .models import Account
from .serializers import AccountSerializerInSearch, AccountDetailSerializerForAnonymousUser, AccountDetailSerializerForNonAnonymousUser, UserDetailSerializer

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

        checkList = {
            "username" : ['[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'],
            "email" : ['^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'],
            "password" : ['^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'],
            "name" : ['[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'],
            "generation" : ['^[1-2]\d{3}$'],
            "student_id" : ['^\d{6,7}$'],
            "gender" : ['^male$', '^female$'],
            "birth" : ['^[1-2]\d{3}-[1-9]-[1-9]', '^[1-2]\d{3}-[0-1]\d-[0-3]\d$'],
            "phone" : ['^\d{10,11}$', '^\d{3}-\d{3,4}-\d{4}$']
        }

        failChecks = []
        for reChecks in checkList:
            isitfail = False
            for reCheck in checkList[reChecks]:
                p = re.compile(reCheck)
                if reChecks == 'username' or reChecks == 'name':
                    if p.findall(data[reChecks]):
                        isitfail = True
                    else:
                        isitfail = False
                        break
                else:
                    if p.match(data[reChecks]):
                        isitfail = False
                        break
                    else:
                        isitfail = True
            if isitfail:
                failChecks.append(reChecks)
        nowYear = datetime.datetime.now().year
        gen = int(data['generation']) - 1992
        if (gen < 1 or gen > nowYear - 1992) and failChecks.count('generation') == 0:
            failChecks.append('generation')
        brth = data['birth'].split('-')
        if ((int(brth[0]) < 1 or int(brth[0]) > nowYear - 18) or (int(brth[1]) < 1 or int(brth[1]) > 12) or (int(brth[2]) < 1 or int(brth[2]) > 31)) and failChecks.count('birth') == 0:
            failChecks.append('birth')
        
        if failChecks:
            msg = ', '.join(failChecks) + '의 값이 잘못되었습니다. 다시 입력해주세요.'
            return JsonResponse({'message': msg}, status=401)

        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({"message": "이미 존재하는 계정 아이디입니다."}, status=401)
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
                    generation=gen,
                    student_id=data['student_id'],
                    gender=data['gender'],
                    birth=data['birth'],
                    phone=data['phone']
                )
            return JsonResponse({"message": "회원으로 가입되셨습니다."}, status=200)

    def get(self, request):
        user = User.objects.values()
        account = Account.objects.values()
        return JsonResponse({"list": list(user) + list(account)}, status=200)


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
            return JsonResponse({"message": "ID와 PASSWORD를 잘못 입력하셨습니다. 다시 입력해주세요"}, status=401)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({"list": list(user)}, status=200)

class UserDetailView(View):
    def get(self, request, author_id):
        author = get_object_or_404(Account, id = author_id)
        response_data = {}
        if request.user.is_active:
            author_data = AccountDetailSerializerForNonAnonymousUser(author).data
            user = User.objects.filter(id=author.user_id).values('email')
            author_data.update(list(user)[0])
        else:
            author_data = AccountDetailSerializerForAnonymousUser(author).data
            
        response_data['author'] = author_data
        return JsonResponse(response_data, status=200)