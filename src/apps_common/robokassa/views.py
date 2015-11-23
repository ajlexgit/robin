from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from .signals import robokassa_paid
from .models import Log
from .conf import EXTRA_PARAMS
from .forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
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

    # попытка получить InvId
    inv_id = data.get('InvId')
    try:
        inv_id = int(inv_id)
    except (TypeError, ValueError):
        inv_id = None

    # log result data
    Log.objects.create(
        inv_id=inv_id,
        step=Log.STEP_RESULT,
        status=Log.STATUS_MESSAGE,
        request=data.urlencode(),
    )

    form = ResultURLForm(data)
    if form.is_valid():
        inv_id = form.cleaned_data['InvId']
        out_sum = form.cleaned_data['OutSum']

        extra = {}
        for key in EXTRA_PARAMS:
            extra[key] = form.cleaned_data.get(key)

        try:
            robokassa_paid.send(sender=ResultURLForm,
                inv_id=inv_id,
                out_sum=out_sum,
                extra=extra,
                site=get_current_site(request),
            )
        except Exception as e:
            # log exception
            Log.objects.create(
                inv_id=inv_id,
                step=Log.STEP_RESULT,
                status=Log.STATUS_ERROR,
                request=data.urlencode(),
                message='Signal exception:\n{}: {}'.format(
                    e.__class__.__name__,
                    ', '.join(e.args),
                )
            )
        else:
            # log success
            Log.objects.create(
                inv_id=inv_id,
                step=Log.STEP_RESULT,
                status=Log.STATUS_SUCCESS,
                request=data.urlencode(),
            )
            return HttpResponse('OK%s' % inv_id)
    else:
        # log form error
        Log.objects.create(
            inv_id=inv_id,
            step=Log.STEP_RESULT,
            status=Log.STATUS_ERROR,
            request=data.urlencode(),
            message='Invalid form:\n{}'.format(
                _log_errors(form.errors),
            )
        )

    return HttpResponse('')


@csrf_exempt
def success(request):
    """ обработчик для SuccessURL """
    data = request.POST if conf.USE_POST else request.GET

    # попытка получить InvId
    inv_id = data.get('InvId')
    try:
        inv_id = int(inv_id)
    except (TypeError, ValueError):
        inv_id = None

    # log success data
    Log.objects.create(
        inv_id=inv_id,
        step=Log.STEP_SUCCESS,
        status=Log.STATUS_MESSAGE,
        request=data.urlencode(),
    )

    form = SuccessRedirectForm(data)
    if form.is_valid():
        inv_id = form.cleaned_data['InvId']

        # log success
        Log.objects.create(
            inv_id=inv_id,
            step=Log.STEP_SUCCESS,
            status=Log.STATUS_SUCCESS,
            request=data.urlencode(),
        )
    else:
        # log form error
        Log.objects.create(
            inv_id=inv_id,
            step=Log.STEP_SUCCESS,
            status=Log.STATUS_ERROR,
            request=data.urlencode(),
            message='Invalid form:\n{}'.format(
                _log_errors(form.errors),
            )
        )

    return redirect(conf.SUCCESS_REDIRECT_URL)


@csrf_exempt
def fail(request):
    """ обработчик для FailURL """
    data = request.POST if conf.USE_POST else request.GET

    # попытка получить InvId
    inv_id = data.get('InvId')
    try:
        inv_id = int(inv_id)
    except (TypeError, ValueError):
        inv_id = None

    # log success data
    Log.objects.create(
        inv_id=inv_id,
        step=Log.STEP_FAIL,
        status=Log.STATUS_MESSAGE,
        request=data.urlencode(),
    )

    form = FailRedirectForm(data)
    if form.is_valid():
        inv_id = form.cleaned_data['InvId']

        # log success
        Log.objects.create(
            inv_id=inv_id,
            step=Log.STEP_FAIL,
            status=Log.STATUS_SUCCESS,
            request=data.urlencode(),
        )
    else:
        # log form error
        Log.objects.create(
            inv_id=inv_id,
            step=Log.STEP_FAIL,
            status=Log.STATUS_ERROR,
            request=data.urlencode(),
            message='Invalid form:\n{}'.format(
                _log_errors(form.errors),
            )
        )

    return redirect(conf.SUCCESS_REDIRECT_URL)

