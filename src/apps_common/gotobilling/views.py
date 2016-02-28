from django.shortcuts import redirect
from .models import Log
from .forms import GotobillingResultForm
from .signals import gotobilling_paid, gotobilling_error
from . import conf


def _log_errors(errors):
    return '\n'.join(
        '{}: {}'.format(
            key,
            ', '.join(errors_list)
        )
        for key, errors_list in errors.items()
    )


def result(request):
    """ Обработчик результата оплаты """
    data = request.GET

    inv_id = data.get('x_invoice_num')

    # log data
    Log.objects.create(
        inv_id=inv_id,
        status=Log.STATUS_MESSAGE,
        request=data.urlencode().replace('&', '\n'),
    )

    form = GotobillingResultForm(data)
    if form.is_valid():
        inv_id = form.cleaned_data['x_invoice_num']
        amount = form.cleaned_data['x_amount']

        response_code = form.cleaned_data['x_response_code']
        if response_code == GotobillingResultForm.RESPONSE_CODE_APPROVED:
            # ------------------------------
            #   Approved
            # ------------------------------
            try:
                gotobilling_paid.send(
                    sender=GotobillingResultForm,
                    inv_id=inv_id,
                    amount=amount,
                )
            except Exception as e:
                # log exception
                Log.objects.create(
                    inv_id=inv_id,
                    status=Log.STATUS_EXCEPTION,
                    request=data.urlencode().replace('&', '\n'),
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
                    request=data.urlencode().replace('&', '\n'),
                )
                return redirect(conf.SUCCESS_REDIRECT_URL)
        else:
            # ------------------------------
            #   Declined или Error
            # ------------------------------
            reason = form.cleaned_data['x_response_reason_text']
            try:
                gotobilling_error.send(
                    sender=GotobillingResultForm,
                    inv_id=inv_id,
                    code=response_code,
                    reason=reason,
                )
            except Exception as e:
                # log exception
                Log.objects.create(
                    inv_id=inv_id,
                    status=Log.STATUS_EXCEPTION,
                    request=data.urlencode().replace('&', '\n'),
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
                    request=data.urlencode().replace('&', '\n'),
                    message=reason,
                )
    else:
        # log form error
        Log.objects.create(
            inv_id=inv_id,
            status=Log.STATUS_ERROR,
            request=data.urlencode().replace('&', '\n'),
            message='Invalid form:\n{}'.format(
                _log_errors(form.errors),
            )
        )

    return redirect(conf.FAIL_REDIRECT_URL)
