import datetime
from hashlib import sha1
from decimal import Decimal
from . import options

CODEPRO_CHOICES = {
    'true': True,
    'false': False,
}

TYPE_CHOICES = {
    'p2p-incoming': 'p2p',
    'card-incoming': 'card',
}


class InvalidPaymentRequest(Exception):
    pass


def validate(request):
    data = {}
    try:
        sha1_hash = request.POST['sha1_hash']
        currency = request.POST['currency']
        notification_type = request.POST['notification_type']

        data['operation_id'] = request.POST['operation_id']
        data['codepro'] = request.POST['codepro']
        data['sender'] = request.POST['sender']
        data['amount'] = request.POST['amount']
        data['label'] = request.POST['label']
        data['datetime'] = request.POST['datetime']
    except KeyError as e:
        raise InvalidPaymentRequest('Required: %s' % e)

    hasher = sha1()
    hasher.update('&'.join((
        notification_type,
        data['operation_id'],
        data['amount'],
        currency,
        data['datetime'],
        data['sender'],
        data['codepro'],
        options.SECRET,
        data['label'],
    )).encode())
    if hasher.hexdigest() != sha1_hash:
        raise InvalidPaymentRequest('Invalid hash for data: %s' % data)

    try:
        data['datetime'] = datetime.datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise InvalidPaymentRequest('Invalid datetime: %s' % data['datetime'])

    try:
        data['amount'] = Decimal(data['amount'])
    except ValueError:
        raise InvalidPaymentRequest('Invalid amount: %s' % data['amount'])

    if data['codepro'] not in CODEPRO_CHOICES:
        raise InvalidPaymentRequest('Unknown codepro: %s' % data['codepro'])
    else:
        data['codepro'] = CODEPRO_CHOICES[data['codepro']]

    if notification_type not in TYPE_CHOICES:
        raise InvalidPaymentRequest('Unknown notification_type: %s' % notification_type)
    else:
        data['type'] = TYPE_CHOICES[notification_type]

    return data
