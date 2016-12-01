import ipaddress


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
        ip = ipaddress.IPv4Address(x_forwarded_for)
    except ValueError:
        return request.META.get('REMOTE_ADDR')
    else:
        return ip.exploded
