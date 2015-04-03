import os
import hashlib
import tempfile
from django.core.files import File

__all__ = ('upload_chunked_file', 'NotCompleteError')


class NotCompleteError(Exception):
    pass


def upload_chunked_file(request, param):
    """
        Загрузчик файлов, переданных от форм.
        Поддерживает передачу файла по частям.
        
        Пример:
            from libs.upload_chunked_file import upload_chunked_file, NotCompleteError
            ...
            
            try:
                uploaded_file = upload_chunked_file(request, 'image')
            except (LookupError, FileNotFoundError):
                raise Http404
            except NotCompleteError:
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
    file = request.FILES[param]
    
    # Файл передан без применения разделения на части
    if not request.POST.get('chunks'):
        return file
    
    chunk_num = int(request.POST.get('chunk', 0))
    chunk_count = int(request.POST.get('chunks', 1))
    
    # Файл передан целиком в одной части
    if chunk_count == 1:
        tmp = tempfile.NamedTemporaryFile()
        for chunk in file.chunks():
            tmp.write(chunk)
        tmp.seek(0)
        return File(tmp)
    
    realname = request.POST.get('name', file.name)
    basename, ext = os.path.splitext(realname)
    basename = '%s.%s' % (request.session.session_key, basename)
    basename = hashlib.md5(basename.encode()).hexdigest()
    filename = '%s%s' % (basename, ext)
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    tmp = File(open(filepath, 'ab+'))
    if chunk_num == 0:
        tmp.seek(0)
        tmp.truncate()
    for chunk in file.chunks():
        tmp.write(chunk)
    
    if chunk_num < chunk_count - 1:
        tmp.close()
        raise NotCompleteError('%d of %d' % (chunk_num, chunk_count))
    else:
        tmp.seek(0)
        return tmp
        