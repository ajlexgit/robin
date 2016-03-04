from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .signals import robokassa_success
from .models import Log
from .conf import EXTRA_PARAMS
from .forms import ResultURLForm
from . import conf


def _log_errors(errors):
    return '\n'.join(
        '{}: {}'.format(
            key,
            ', '.join(errors_list)
        )
        for key, errors_list in errors.items()
    )


@csrf_exempt
def result(request):
    """ Обработчик для ResultURL """
    data = request.POST if conf.USE_POST else request.GET
    urlencoded = data.urlencode().replace('&', '\n')

    # попытка получить InvId
    inv_id = data.get('InvId')
    try:
        inv_id = int(inv_id)
    except (TypeError, ValueError):
        inv_id = None

    # log result data
    Log.objects.create(
        inv_id=inv_id,
        status=Log.STATUS_MESSAGE,
        request=urlencoded,
    )

    form = ResultURLForm(data)
    if form.is_valid():
        inv_id = form.cleaned_data['InvId']

        extra = {}
        for key in EXTRA_PARAMS:
            extra[key] = form.cleaned_data.get(key)

        try:
            robokassa_success.send(
                sender=Log,
                request=request,
                inv_id=inv_id,
                extra=extra,
            )
        except Exception as e:
            # log exception
            Log.objects.create(
                inv_id=inv_id,
                status=Log.STATUS_EXCEPTION,
                request=urlencoded,
                message='Signal exception:\n{}: {}'.format(
                    e.__class__.__name__,
                    ', '.join(e.args),
                )
            )
        else:
            # log success
            Log.objects.create(
                inv_id=inv_id,
                status=Log.STATUS_SUCCESS,
                request=urlencoded,
            )
            return HttpResponse('OK%s' % inv_id)
    else:
        # log form error
        Log.objects.create(
            inv_id=inv_id,
            status=Log.STATUS_ERROR,
            request=urlencoded,
            message='Invalid form:\n{}'.format(
                _log_errors(form.errors),
            )
        )

    return HttpResponse('')
