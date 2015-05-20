class ProtectedModelFormMixin:
    """
        Миксина формы, которая запещает менять значения указанных
        полей при добавлении или редактировании. Если в форме указано
        новое значение защащенного поля, это значение будет проигнорировано
        и вместо него будет использоване значение по умолчанию.
    """
    protect_add_fields = ()
    protect_change_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = self.data.dict() if self.data else {}

        for fieldname in self.fields:
            if self.prefix is not None:
                prefixed_fieldname = '-'.join((self.prefix, fieldname))
            else:
                prefixed_fieldname = fieldname

            if self.instance.pk:
                # редактирование
                if fieldname in self.protect_change_fields:
                    if fieldname in self.initial:
                        self.data[prefixed_fieldname] = self.initial[fieldname]
                    elif prefixed_fieldname in self.data:
                        del self.data[prefixed_fieldname]
            else:
                # добавление
                if fieldname in self.protect_add_fields:
                    if fieldname in self.initial:
                        self.data[prefixed_fieldname] = self.initial[fieldname]
                    elif prefixed_fieldname in self.data:
                        del self.data[prefixed_fieldname]
