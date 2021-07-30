import datetime
import re

from django.core.exceptions import ValidationError


def validate_names(value):
    error_messages = {
        "special_char" : "ID나 이름에는 특수문자가 허용되지 않습니다."
    }
    if re.findall('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', value):
        raise ValidationError(error_messages['special_char'])
    return value

def validate_password(value):
    error_messages = {
        "wrong_password" : "비밀번호는 최소 하나의 문자, 하나의 숫자, 하나의 특수문자를 포함하며 8글자 이상이어야 합니다."
    }
    if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', value):
        raise ValidationError(error_messages['wrong_password'])
    return value

def validate_student_id(value):
    error_messages = {
        "wrong_student_id" : "학번은 6~7글자의 숫자이어야 합니다."
    }
    if not re.match('^\d{6,7}$', value):
        raise ValidationError(error_messages['wrong_student_id'])
    return value

def validate_birth(value):
    error_messages = {
        "wrong_year" : "생년 입력이 잘못되었습니다. %(year)s년생부터 가입이 가능합니다."
    }
    birth = str(value).split('-')
    now_year = int(datetime.datetime.now().year)
    if int(birth[0]) > now_year - 18:
        raise ValidationError(error_messages['wrong_year'] % {"year" : now_year - 18})
    return value

def validate_phone(value):
    error_messages = {
        "wrong_phone" : "전화번호는 000-000-0000나 000-0000-0000 형식이어야 합니다."
    }
    if not re.match('^\d{3}-\d{3,4}-\d{4}$', value):
        raise ValidationError(error_messages['wrong_phone'])
    return value