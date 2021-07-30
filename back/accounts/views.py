import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

from .forms import AccountCreateForm, AccountUpdateForm
from .models import Account
from .serializers import AccountDetailSerializerForAnonymousUser, AccountDetailSerializerForNonAnonymousUser


class UserRegisterView(View):
    def post(self, request):
        success_message = "회원으로 가입되셨습니다."
        error_messages = {
            'regex_fail' : "'%(regex_fails)s'의 값이 잘못되었습니다. 다시 입력해주세요.",
            'already_exist_username' : "이미 존재하는 계정 아이디입니다.",
            'already_exist_email' : "이미 존재하는 이메일입니다.",
            'already_exist_student_id' : "이미 존재하는 학번입니다.",
            'create_fail' : "회원 가입에 실패했습니다. 확인 후 다시 시도해주세요.",
        }

        data = json.loads(request.body)

        form = AccountCreateForm(data)
        if not form.is_valid():
            return JsonResponse({"message": form.errors}, status=400)

        if User.objects.filter(username=form.cleaned_data['username']).exists():
            return JsonResponse({"message": error_messages['already_exist_username']}, status=400)
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            return JsonResponse({"message": error_messages['already_exist_email']}, status=400)
        if Account.objects.filter(student_id=form.cleaned_data['student_id']).exists():
            return JsonResponse({"message": error_messages['already_exist_student_id']}, status=400)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    is_active=False
                )
                Account.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    generation=form.cleaned_data['generation'] - 1992,
                    student_id=form.cleaned_data['student_id'],
                    gender=form.cleaned_data['gender'],
                    birth=form.cleaned_data['birth'],
                    phone=form.cleaned_data['phone']
                )
        except:
            return JsonResponse({"message": error_messages['create_fail']}, status=400)
        return JsonResponse({"message": success_message}, status=200)


class UserDetailView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request, account_id):
        success_message = "'%(name)s' 님의 회원 정보가 수정되었습니다."
        error_messages = {
            "not_exist_account" : "수정하려는 회원의 정보가 존재하지 않습니다. 확인 후 다시 시도해주세요.",
            "not_exist_user" : "해당 계정 정보가 존재하지 않습니다. 관리자에게 연락해주세요.",
            "not_permitted" : "해당 계정은 회원 수정 권한이 없습니다. 수정하려는 계정이나 관리자 계정으로 로그인 후 다시 시도해주세요.",
            'already_exist_email' : "이미 존재하는 이메일입니다.",
            'already_exist_student_id' : "이미 존재하는 학번입니다.",
            "update_fail" : "회원 정보를 수정하는 도중에 오류가 발생했습니다. 다시 시도해주세요."
        }

        data = json.loads(request.body)

        if account_id != request.user.id and not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        author = Account.objects.filter(id=account_id)
        if not author.exists():
            return JsonResponse({"message":error_messages['not_exist_account']}, status=404)
        author = author[0]
        user = User.objects.filter(id=author.user_id)
        if not user.exists():
            return JsonResponse({"message":error_messages['not_exist_user']}, status=404)
        user = user[0]
        
        form = AccountUpdateForm(data)
        if not form.is_valid():
            return JsonResponse({"message":form.errors}, status=400)

        if User.objects.filter(email=form.cleaned_data['email']).exists():
            return JsonResponse({"message":error_messages['already_exist_email']}, status=400)
        if Account.objects.filter(student_id=form.cleaned_data['student_id']).exists():
            return JsonResponse({"message":error_messages['already_exist_student_id']}, status=400)

        for key, value in form.cleaned_data.items():
            if key == 'email' and value:
                user.email = value
            elif key == 'name' and value:
                author.name = value
            elif key == 'generation' and value:
                author.generation = value - 1992
            elif key == 'student_id' and value:
                author.student_id = value
            elif key == 'gender' and value:
                author.gender = value
            elif key == 'birth' and value:
                author.birth = value
            elif key == 'phone' and value:
                author.phone = value
            elif key == 'password' and value:
                user.set_password(value)

        try:
            with transaction.atomic():
                user.save()
                author.save()
        except:
            return JsonResponse({"message":error_messages['update_fail']}, status=400)
        return JsonResponse({"message":success_message % {"name" : user.username}}, status=200)

    def get(self, request, account_id):
        author = get_object_or_404(Account, id=account_id)
        if request.user.is_active:
            response_data = AccountDetailSerializerForNonAnonymousUser(author).data
            user = User.objects.filter(id=author.user_id).values('email')
            response_data.update(list(user)[0])
        else:
            response_data = AccountDetailSerializerForAnonymousUser(author).data
        return JsonResponse(response_data, status=200)

    @method_decorator(login_required, name="dispatch")
    def delete(self, request, account_id):
        success_message = "'%(user_name)s' 회원이 삭제되었습니다."
        error_messages = {
            "not_permitted" : "계정 삭제 권한이 없습니다. 삭제할 계정이나 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "not_exist_account" : "해당 회원이 존재하지 않습니다.",
            "not_exist_user" : "해당 계정 정보가 존재하지 않습니다. 관리자에게 연락해주세요.",
            "delete_fail" : "회원을 삭제하는 도중에 오류가 발생했습니다. 다시 시도해주세요."
        }

        if account_id != request.user.id and not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=401)

        author = Account.objects.filter(id=account_id)
        if not author.exists():
            return JsonResponse({"message": error_messages['not_exist_account']}, status=404)
        author = author[0]
        user = User.objects.filter(id=author.user_id)
        if not user.exists():
            return JsonResponse({"message": error_messages['not_exist_user']}, status=404)
        user = user[0]

        try:
            with transaction.atomic():
                user.delete()
                author.delete()
        except:
            return JsonResponse({"message": error_messages['delete_fail']}, status=400)
        return JsonResponse({"message": success_message % {"user_name" : user.username}}, status=200)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = authenticate(
            username=data['username'], 
            password=data['password']
        )
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "로그인에 성공하셨습니다."}, status=200)
        else:
            return JsonResponse({"message": "아이디나 비밀번호가 잘못되었습니다. 다시 입력해주세요."}, status=401)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({"list": list(user)}, status=200)


class LogoutView(View):
    @method_decorator(login_required, name="dispatch")
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "로그아웃 되었습니다."}, status=200)


class PermissionView(View):
    @method_decorator(login_required, name="dispatch")
    def patch(self, request, account_id):
        success_message = "'%(username)s' 님이 정상적으로 승인되었습니다"
        error_messages = {
            "already_permitted" : "'%(username)s' 님은 이미 승인된 계정입니다.",
            "not_permitted" : "해당 계정은 승인 권한이 없습니다. 관리자 계정으로 로그인 후 다시 시도해주세요.",
            "not_exist_account" : "해당 회원이 존재하지 않습니다.",
            "not_exist_user" : "해당 계정 정보가 존재하지 않습니다.",
            "permit_user_fail" : "회원을 승인하던 도중에 오류가 발생했습니다. 다시 시도해주세요."
        }

        if not request.user.is_superuser:
            return JsonResponse({"message":error_messages['not_permitted']}, status=403)

        account = Account.objects.filter(id=account_id)
        if not account.exists():
            return JsonResponse({"message":error_messages['not_exist_account']}, status=404)
        account = account[0]
        user = User.objects.filter(id=account.user_id)
        if not user.exists():
            return JsonResponse({"message":error_messages['not_exist_user']}, status=404)
        user = user[0]

        if user.is_active:
            return JsonResponse({"message": error_messages['already_permitted'] % {"username":user.username}}, status=406)

        user.is_active = True
        try:
            user.save(update_fields=['is_active'])
        except:
            return JsonResponse({"message": error_messages['permit_user_fail']}, status=400)
        return JsonResponse({"message": success_message % {"username":user.username}}, status=200)