from django.shortcuts import redirect


def away(request):
    url = request.GET.get('url') or 'index'
    return redirect(url)