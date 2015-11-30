import os
import mimetypes
from urllib.parse import quote
from django.http import HttpResponse


def AttachmentResponse(request, file, original_filename=None):
    """
        Response, заставляющий браузер скачать файл.

        Пример:
            # views.py
            def download(request, file_id):
                page_file = get_object_or_404(PageFile, pk=file_id)
                return AttachmentResponse(request, page_file.file)
    """
    if isinstance(file, str):
        file = open(file, 'rb')

    response = HttpResponse(file)

    if original_filename is None:
        original_filename = os.path.basename(file.name)

    type_name, encoding = mimetypes.guess_type(original_filename)
    if type_name is None:
        type_name = 'application/octet-stream'
    response['Content-Type'] = type_name
    response['Content-Length'] = str(len(response.content))
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if 'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % quote(original_filename)
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response
