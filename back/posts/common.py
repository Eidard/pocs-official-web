import datetime
import os
import uuid
import hashlib
import bleach

from .markdown import *
from django.conf import settings


def file_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime("%Y/%m/%d")
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = f"{uuid.uuid4().hex}_{suffix}.{ext}"
    return os.path.join(f'{settings.FILE_MEDIA_DIR}/' + filepath, filename)

def is_dir_empty(path):
    return next(os.scandir(path), None) is None

def remove_saved_files_and_empty_dirs(savedFilePaths):
    filePaths = []
    for filePath in savedFilePaths:
        if filePath == f'media/{settings.DEFAULT_IMAGE_RELATIVE_PATH}':
            continue
        if os.path.exists(filePath):
            os.remove(filePath)
            filePaths.append(filePath[:filePath.rfind('/')])
    filePaths = tuple(set(filePaths))
    for fp in filePaths:
        while True:
            if fp == f'media/{settings.BACKGROUND_IMAGES_MEDIA_DIR}' or fp == f'media/{settings.FILE_MEDIA_DIR}' or fp == 'media':
                break
            if os.path.exists(fp) and is_dir_empty(fp):
                os.rmdir(fp)
            if fp.rfind('/') == -1:
                break
            fp = fp[:fp.rfind('/')]

def get_file_hash(fileInstance):
    ctx = hashlib.sha256()
    if fileInstance.multiple_chunks():
        for data in fileInstance.chunks():
            ctx.update(data)
    else:
        ctx.update(fileInstance.read())
    return ctx.hexdigest()

def unmarkdown(text):
    return unmark(text)

MARKDOWN_TAGS = (
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p',
    'em', 'strong', 'u',
    'ol', 'ul', 'li',
    'a',
    'img',
    'pre', 'code',
    'table', 'thead', 'tr', 'th', 'td', 'tbody',
    'blockquote',
    'br', 'hr',
)

MARKDOWN_ATTRIBUTES_PER_TAG = {
    'img' : ['alt', 'src', 'title'],
    'a' : ['href'],
    'th' : ['align'],
    'td' : ['align'],
}

def trans_markdown_to_html_and_bleach(text):
    html_text = markdown(text, extensions=['tables'])
    return bleach.clean(
        html_text,
        strip_comments=False,
        tags=MARKDOWN_TAGS,
        attributes=MARKDOWN_ATTRIBUTES_PER_TAG
    )