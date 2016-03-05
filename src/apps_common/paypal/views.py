from requests import post as http_post
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Log
from .forms import PayPalResultForm
from .signals import paypal_success, paypal_error
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
    """ Обработчик результата оплаты """
    data = request.POST
    urlencoded = data.urlencode().replace('&', '\n')

    inv_id = data.get('invoice')

    # log data
    Log.objects.create(
        inv_id=inv_id,
        status=Log.STATUS_MESSAGE,
        request=urlencoded,
    )

    form = PayPalResultForm(data)
    if form.is_valid():
        payment_status = form.cleaned_data['payment_status']
        receiver_email = form.cleaned_data['receiver_email']
        invoice = form.cleaned_data['invoice']

        resp = http_post(conf.FORM_TARGET, 'cmd=_notify-validate&' + data.urlencode())
        if (resp.text == 'VERIFIED'
            and payment_status.lower() == 'completed'
            and receiver_email.lower() == conf.EMAIL.lower()):

            try:
                paypal_success.send(
                    sender=Log,
                    invoice=invoice,
                    request=request,
                )
            except Exception as e:
                # log exception
                Log.objects.create(
                    inv_id=invoice,
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
                    inv_id=invoice,
                    status=Log.STATUS_SUCCESS,
                    request=urlencoded,
                )
        else:
            try:
                paypal_error.send(
                    sender=Log,
                    invoice=invoice,
                    request=request,
                )
            except Exception as e:
                # log exception
                Log.objects.create(
                    inv_id=invoice,
                    status=Log.STATUS_EXCEPTION,
                    request=urlencoded,
                    message='Signal exception:\n{}: {}'.format(
                        e.__class__.__name__,
                        ', '.join(e.args),
                    )
                )
            else:
                # log fail
                Log.objects.create(
                    inv_id=inv_id,
                    status=Log.STATUS_ERROR,
                    request=urlencoded,
                    message='Not verified',
                )

            return redirect(conf.FAIL_URL)
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

    # Показываем Success даже если форма не валидна,
    # чтобы не пугать пользователя, если, например,
    # хэш рассчитывается неправильно
    return redirect(conf.SUCCESS_URL)
