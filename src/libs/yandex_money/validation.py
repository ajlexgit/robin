from hashlib import sha1
from . import options


class InvalidPaymentRequest(Exception):
    pass


def validate(request):
    try:
        sha1_hash = request.POST['sha1_hash']
        currency = request.POST['currency']
        operation_id = request.POST['operation_id']
        notification_type = request.POST['notification_type']
        codepro = request.POST['codepro']
        sender = request.POST['sender']
        amount = request.POST['amount']
        label = request.POST['label']
        datetime = request.POST['datetime']
    except KeyError as e:
        raise InvalidPaymentRequest('Required: %s' % e)

    hasher = sha1()
    data = '&'.join((
        notification_type, operation_id, amount, currency,
        datetime, sender, codepro, options.SECRET, label
    ))
    hasher.update(data.encode())
    if hasher.hexdigest() != sha1_hash:
        raise InvalidPaymentRequest('Invalid hash')
