import datetime
import os
import uuid

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