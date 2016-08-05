from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from libs.download import AttachmentResponse
from .models import PageFile


@never_cache
def download(request, file_id):
    page_file = get_object_or_404(PageFile, pk=file_id)
    return AttachmentResponse(request, page_file.file)
