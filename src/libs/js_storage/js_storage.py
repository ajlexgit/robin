import json


class JSStorage(dict):
    def out(self):
        """ Вывод переменных в шаблон """
        object_body = ','.join(
            '"{0}": {1}'.format(key, json.dumps(val)) for key, val in self.items()
        )
        return 'var js_storage = {{ {0} }}'.format(object_body)
