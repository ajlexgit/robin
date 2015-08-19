import os
import mimetypes
from urllib.parse import quote
from django.http import HttpResponse


def DownloadResponse(request, file_path, original_filename):
    """
        Response, заставляющий браузер скачать файл
    """
    with open(file_path, 'rb') as fp:
        response = HttpResponse(fp.read())

    type_name, encoding = mimetypes.guess_type(original_filename)
    if type_name is None:
        type_name = 'application/octet-stream'
    response['Content-Type'] = type_name
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if 'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif 'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response