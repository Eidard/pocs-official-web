import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_tags(value):
    error_messages = {
        'type_error': '입력한 태그(들) 중 형식이 올바르지 않는 태그가 있습니다. 확인 후 다시 시도해주세요.',
        'empty_value' : '입력한 태그(들) 중 빈 태그가 입력되었습니다. 확인 후 다시 시도해주세요.',
        'max_length' : f'태그는 글 당 최대 {settings.MAX_TAG_COUNT_IN_POST}개까지만 입력이 가능합니다. 확인 후 다시 시도해주세요.'
    }
    tag_regex = '^[ a-zA-Z0-9가-힣-]+$'
    tags = list(map(lambda x : x.strip(), value.split(',')))
    if len(tags) > settings.MAX_TAG_COUNT_IN_POST:
        raise ValidationError(error_messages['max_length'])
    for tag in tags:
        if not tag:
            raise ValidationError(error_messages['empty_value'])
        if not re.search(tag_regex, tag):
            raise ValidationError(error_messages['type_error'])
    return value


class FileValidator(FileExtensionValidator):
    special_char_message = "'-', '.', '_', '!', '(', ')', '[', ']'"
    special_char_regex = '[=+,#/\?:^$@*\"※~&%ㆍ』\\‘|\<\>`\'…》]'
    dotdot_regex = '[.]{2}'
    
    error_messages = {
        'size_zero' : "첨부한 파일 중 용량이 '0'바이트인 파일이 있습니다. 해당 파일(들)을 제외하고 다시 시도해주세요.",
        'special_char' : f"파일 이름에 {special_char_message}를 제외한 특수문자가 들어있는 파일은 업로드가 불가합니다. 해당 파일 이름을 변경하고 다시 시도해주세요.",
        'dotdot_char' : "파일 이름에 '..'이 들어있는 파일은 업로드가 불가합니다. 해당 파일 이름을 변경하고 다시 시도해주세요.",
        'extension' : "파일은 '%(allowed_extensions)s'의 확장자를 가진 파일만 업로드가 가능합니다. 확인 후 다시 시도해주세요."
    }
    
    def __init__(self, allowed_extensions):
        super().__init__(
            allowed_extensions=allowed_extensions, 
            message=self.error_messages['extension'] % {'allowed_extensions':', '.join(allowed_extensions)}
        )

    def __call__(self, value):
        super().__call__(value)
        if re.search(self.special_char_regex, value.name):
            raise ValidationError(self.error_messages['special_char'])
        if re.search(self.dotdot_regex, value.name):
            raise ValidationError(self.error_messages['dotdot_char'])
        if value.size == 0:
            raise ValidationError(self.error_messages['size_zero'])
        return value