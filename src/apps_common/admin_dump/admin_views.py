from django.contrib import admin
from django.shortcuts import render


@admin.site.admin_view
def index(request):
    return render(request, 'admin_dump/admin/index.html', {})


@admin.site.admin_view
def make_dump(request):
    pass
