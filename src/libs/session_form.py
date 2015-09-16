"""
    Миксина формы, которая добавляет методы сохранения данных в сессию и извлечения
    из сессии.

    Ошибки формы тоже сохраняются в сессию и восстанавливаются вместе с данными.
    Но они восстанавливаются только один раз (для POST с редиректом на GET).

    Ключом сессии является хэш от класса формы и её префикса.

    Примеры:
        # GET
        form = SessionForm(initial={'name': 'Pix'})
        form.load_from_session(request)
        ...

        # POST
        form = SessionForm(data=request.POST, initial={'name': 'Pix'})
        if form.is_valid():
            form.remove_from_session(request)
            ...
        else:
            form.save_to_session(request)
            ...
"""

import time
import hashlib
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.http.response import HttpResponseRedirect


class BaseMixin:
    # Время хранения данных в сессии
    max_store_time = 10 * 60

    # Поля, чьи значения не нужно сохранять
    unstored_fields = ()

    # Идентификатор для определения одинаковых форм (вместо имени класса)
    session_store_id = None

    @cached_property
    def form_data_key(self):
        """ Построение ключа сессии, где хранятся данные формы """
        return self.get_class_key(str(self.prefix or ''))

    @classmethod
    def get_class_key(cls, prefix=''):
        if cls.session_store_id:
            session_store_id = cls.session_store_id
        else:
            session_store_id = '.'.join((cls.__module__, cls.__qualname__))
        hash_data = (session_store_id, prefix)
        hash_data_bytes = ':'.join(hash_data).encode()
        return hashlib.sha1(hash_data_bytes).hexdigest()

    def _storing_form_data(self, form):
        """ Получение данных одной формы для сохранения в сессию """
        data = {}
        prefix = form.prefix + '-' if form.prefix else ''
        for field in form.fields:
            if field not in self.unstored_fields:
                data[field] = form.data.get(prefix + field)
        return data

    @staticmethod
    def _storing_form_errors(form):
        """ Получение ошибок одной формы для сохранения в сессию """
        result = {}

        if form._errors is None:
            return result

        for field, error_list in form.errors.items():
            field_errors = []
            for error in error_list.as_data():
                field_errors.append({
                    'message': str(error.message) or '',
                    'code': error.code or '',
                    'params': error.params,
                })
            result[field] = field_errors
        return result

    @property
    def storing_data(self):
        raise NotImplementedError

    def save_to_session(self, request):
        """ Сохранение данных и ошибок формы/формсета в сессию """
        request.session[self.form_data_key] = self.storing_data

    @staticmethod
    def _load_form_errors(form, stored_errors):
        """ Восстановление ошибок одной формы """
        form.cleaned_data = {}
        for field, errors in stored_errors.items():
            for error in errors:
                form.add_error(field, ValidationError(**error))

    def _load_errors(self, stored):
        raise NotImplementedError

    def _load_data(self, stored):
        raise NotImplementedError

    def load_from_session(self, request):
        """ Загрузка данных и ошибок формы/формсета из сессии """
        stored = request.session.get(self.form_data_key, {})
        store_time = stored.get('_store_time', 0)
        if store_time and (int(time.time()) - store_time < self.max_store_time):
            self._load_data(stored)
            self._load_errors(stored)

            # Перезапись данных для удаления ошибок из сессии
            request.session[self.form_data_key] = stored
        else:
            # Удаление устаревших данных
            self.remove_from_session(request)

    def remove_from_session(self, request):
        """ Удаление данных и ошибок формы/формсета из сессии """
        try:
            del request.session[self.form_data_key]
        except KeyError:
            pass


class SessionStoredFormMixin(BaseMixin):
    @property
    def storing_data(self):
        """ Получение данных формы для сохранения в сессию """
        return {
            '_store_time': int(time.time()),
            'data': self._storing_form_data(self),
            'errors': self._storing_form_errors(self),
        }

    def _load_errors(self, stored):
        """ Восстановление ошибок формы """
        stored_errors = stored.pop('errors', {})
        if stored_errors:
            self._load_form_errors(self, stored_errors)

    def _load_data(self, stored):
        """ Восстановление данных формы """
        self.initial.update(stored.get('data', {}))

    def is_valid(self):
        # Если не очистить ошибки - ошибки валидации добавятся
        # к ошибкам, восстановленным из сессии
        self._errors = None
        return super().is_valid()


class SessionStoredFormSetMixin(BaseMixin):
    @property
    def storing_data(self):
        """ Получение данных формсета для сохранения в сессию """
        forms_data = []
        forms_errors = []
        for index, form in enumerate(self.forms):
            if index >= self.min_num and not form.has_changed():
                continue

            forms_data.append(self._storing_form_data(form))
            forms_errors.append(self._storing_form_errors(form))

        non_form_errors = []
        for error in self.non_form_errors().as_data():
            non_form_errors.append({
                'message': str(error.message) or '',
                'code': error.code or '',
                'params': error.params or '',
            })

        return {
            '_store_time': int(time.time()),
            'data': forms_data,
            'errors': forms_errors,
            'non_form_errors': non_form_errors,
        }

    def _load_errors(self, stored):
        """ Восстановление ошибок формсета """
        stored_errors = stored.pop('errors', [])
        for form, form_errors in zip(self.forms, stored_errors):
            self._load_form_errors(form, form_errors)

        non_form_errors = stored.pop('non_form_errors', [])
        self._non_form_errors = self.error_class([
            ValidationError(**error_data) for error_data in non_form_errors
        ])

    def _load_data(self, stored):
        """ Восстановление данных формсета """
        self.initial.update(stored.get('data', []))

    def is_valid(self):
        # Если не очистить ошибки - ошибки валидации добавятся
        # к ошибкам, восстановленным из сессии
        for form in self.forms:
            form._errors = None

        return super().is_valid()

    @cached_property
    def is_max_forms(self):
        """ Проверка достижения максимального кол-ва форм """
        return self.total_form_count() >= self.max_num

    @cached_property
    def is_min_forms(self):
        """ Проверка достижения минимального кол-ва форм """
        return self.total_form_count() <= self.min_num


class SessionFormView(FormView):

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.load_from_session(self.request)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.remove_from_session(self.request)
            return self.form_valid(form)
        else:
            form.save_to_session(self.request)
            return self.form_invalid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.request.build_absolute_uri())
