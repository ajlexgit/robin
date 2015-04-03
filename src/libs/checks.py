from django.core import checks

"""
    Набор миксин, упрощающих проверки моделей и полей.
    
    Пример проверки модели:
        class MyModel(ModelChecksMixin, models.Model):
            ...
            @classmethod
            def custom_check(cls):
                errors = []
                if not isinstance(cls.TYPE, int):
                    errors.append(
                        cls.check_error('TYPE should be a number')
                    )
                return errors
    
    Пример проверки поля:
        class MyField(FieldChecksMixin, Field):
            ...
            def custom_check(self):
                errors = []
                if not isinstance(self.min_length, int):
                    errors.append(
                        self.check_error('min_length should be a number')
                    )
                return errors
"""

class ModelChecksMixin:
    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls.custom_check())
        return errors
    
    @classmethod
    def custom_check(cls):
        """ 
            Проверка модели.
            Должен вернуть список ошибок в виде экземпляров checks.Error
        """
        raise NotImplementedError

    @classmethod
    def check_error(cls, message, obj=None, **kwargs):
        return checks.Error(
            message,
            obj=obj or cls,
            **kwargs
        )


class FieldChecksMixin:
    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self.custom_check())
        return errors
    
    def custom_check(self):
        """ 
            Проверка поля.
            Должен вернуть список ошибок в виде экземпляров checks.Error
        """
        raise NotImplementedError
    
    def check_error(self, message, obj=None, **kwargs):
        return checks.Error(
            message,
            obj=obj or self,
            **kwargs
        )
