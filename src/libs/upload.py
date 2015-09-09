import os
import hashlib
import requests
import tempfile
from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile, InMemoryUploadedFile

__all__ = ('upload_file', 'upload_chunked_file', 'NotLastChunk', 'FileMissingError')


class NotLastChunk(Exception):
    pass

class FileMissingError(Exception):
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath = filepath

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.filepath)


class TempUploadedFile(UploadedFile):
    """ Файл, удаляющийся после закрытия """
    def close(self):
        super().close()
        if os.path.exists(self.file.name):
            os.unlink(self.file.name)

    # Need to ensure the file is deleted on __del__
    def __del__(self):
        self.close()


def upload_file(url, timeout=5):
    """
        Загрузка файла по урлу во временный файл.

        Пример:
            from libs.upload import upload_file
            ...
            
            try:
                uploaded_file = upload_file('http://host.ru/image.jpg')
            except ConnectionError as e:
                return JsonResponse({
                    'message': str(e),
                }, status=400)

            request.user.avatar.save(uploaded_file.name, uploaded_file, save=False)
            uploaded_file.close()
            
            try:
                request.user.avatar.field.clean(request.user.avatar, request.user)
            except ValidationError as e:
                request.user.avatar.delete(save=False)
                return JsonResponse({
                    'message': ', '.join(e.messages),
                }, status=400)

            request.user.avatar.clean()
            request.user.avatar.save()
    """
    request = requests.get(url, stream=True, timeout=timeout, headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    })
    if not request.ok:
        raise ConnectionError('Wrong upload status: %s' % request.status_code)

    file_name = url.split('/')[-1]
    content_type = request.headers.get('content-type')
    file_size = request.headers.get('content-length')
    charset = (request.encoding or 'utf-8').lower()

    tmp = TemporaryUploadedFile(
        file_name, content_type, file_size,
        charset, {}
    )
    for block in request.iter_content(8 * 1024):
        if not block:
            break
        tmp.write(block)
    tmp.seek(0)
    tmp.flush()
    return tmp


def upload_chunked_file(request, param_name, allow_memory=True):
    """
        Загрузчик файлов, переданных от форм.
        Поддерживает передачу файла по частям.

        Возвращает обертку над файлом (возможно в памяти), удаляющимся после закрытия.

        Если allow_memory = False, то мелкие файлы, которые Django сохраняет в память,
        будут принудительно сохранены во временные файлы на диске.

        Пример:
            from libs.upload import upload_chunked_file, NotLastChunk, FileMissingError
            ...

            try:
                uploaded_file = upload_chunked_file(request, 'image')
            except FileMissingError as e:
                return JsonResponse({
                    'message': str(e),
                }, status=400)
            except NotLastChunk:
                return HttpResponse()

            request.user.avatar.save(uploaded_file.name, uploaded_file, save=False)
            uploaded_file.close()

            try:
                request.user.avatar.field.clean(request.user.avatar, request.user)
            except ValidationError as e:
                request.user.avatar.delete(save=False)
                return JsonResponse({
                    'message': ', '.join(e.messages),
                }, status=400)

            request.user.avatar.clean()
            request.user.avatar.save()

    """
    file = request.FILES[param_name]

    chunk_num = int(request.POST.get('chunk', 0))
    chunk_count = int(request.POST.get('chunks', 1))

    if chunk_count == 1:
        # файл одним куском
        if not isinstance(file, InMemoryUploadedFile):
            return file
        elif allow_memory:
            return file
        else:
            # принудительное сохранение в файл
            tmp = TemporaryUploadedFile(
                file.name, file.content_type, file.size,
                file.charset, file.content_type_extra
            )
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp.seek(0)
            tmp.flush()
            return tmp
    else:
        # pluploader отправляет имя "blob"
        file.name = os.path.basename(request.POST.get('name', file.name))

        # генерируем имя, которое можно восстановить при получении
        # следующих чанков
        name, ext = os.path.splitext(file.name)
        hashname = '%s.%s' % (request.session.session_key, name)
        hashname = hashlib.md5(hashname.encode()).hexdigest()
        tempfile_name = '%s.upload%s' % (hashname, ext)
        tempfile_path = os.path.join(tempfile.gettempdir(), tempfile_name)

        if chunk_num > 0:
            if not os.path.exists(tempfile_path):
                raise FileMissingError(tempfile_path)

        tmp = open(tempfile_path, 'ab+')
        if chunk_num == 0:
            tmp.seek(0)
            tmp.truncate()
        for chunk in file.chunks():
            tmp.write(chunk)

        if chunk_num < chunk_count - 1:
            tmp.close()
            raise NotLastChunk('%d of %d' % (chunk_num + 1, chunk_count))

        tmp.seek(0)
        tmp.flush()

        file_info = os.stat(tempfile_path)
        return TempUploadedFile(
            tmp,
            name=file.name,
            content_type=file.content_type,
            size=file_info.st_size,
            charset=file.charset,
            content_type_extra=file.content_type_extra
        )
