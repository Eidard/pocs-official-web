import datetime
import os
import uuid

FiLE_MEDIA_DIR = 'files'
BACKGROUND_IMAGES_MEDIA_DIR = 'backgroundImages'

def file_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime("%Y/%m/%d")
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = f"{uuid.uuid4().hex}_{suffix}.{ext}"
    return os.path.join(f'{FiLE_MEDIA_DIR}/' + filepath, filename)

def is_dir_empty(path):
    return next(os.scandir(path), None) is None

def remove_saved_files_and_empty_dirs(savedFilePaths):
    filePaths = []
    for filePath in savedFilePaths:
        os.remove(filePath)
        filePaths.append(filePath[:filePath.rfind('/')])
    filePaths = tuple(set(filePaths))
    for fp in filePaths:
        while True:
            if fp == f'media/{BACKGROUND_IMAGES_MEDIA_DIR}' or fp == f'media/{FiLE_MEDIA_DIR}':
                break
            if is_dir_empty(fp):
                os.rmdir(fp)
            fp = fp[:fp.rfind('/')]