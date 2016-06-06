from collections import namedtuple
from django.db import models
from django.utils.html import escape


AttrType = namedtuple('AttrType', 'BOOL INT BIGINT FLOAT STRING TIMESTAMP MULTI JSON')
ATTR_TYPE = AttrType(
    BOOL='bool',
    INT='int',
    BIGINT='bigint',
    FLOAT='float',
    STRING='string',
    TIMESTAMP='timestamp',
    MULTI='multi',
    JSON='json',
)

# Словарь всех индексов. Заполняется в apps.py
ALL_INDEXES = {}


class SphinxXMLIndex:
    name = ''
    model = None

    def __init__(self):
        self.fields = {}
        self.attrs = {}
        if not issubclass(self.model, models.Model):
            raise AttributeError("SphinxXMLIndex requires model attribute")

    def add_fields(self, name, is_attribute=False):
        """ Добавление поля для полнотекстового поиска """
        self.fields[name] = is_attribute

    def add_attr(self, name, attr_type=ATTR_TYPE.STRING, default=None):
        """ Добавление аттрибута индекса """
        self.attrs[name] = (attr_type, default)

    def build_schema(self):
        """ Генератор схемы индекса """
        yield """<sphinx:schema>"""

        # Fields
        for name, is_attribute in self.fields.items():
            if is_attribute:
                yield """<sphinx:field name="{}" attr="string"/>""".format(name)
            else:
                yield """<sphinx:field name="{}"/>""".format(name)

        # Content Type
        yield """<sphinx:attr name="{}" type="string" default="{}"/>""".format(
            'index_name',
            self.name
        )

        # Attributes
        for name, info in self.attrs.items():
            if info[1] is None:
                yield """<sphinx:attr name="{}" type="{}"/>""".format(name, info[0])
            else:
                yield """<sphinx:attr name="{}" type="{}" default="{}"/>""".format(name, info[0], info[1])

        yield """</sphinx:schema>"""

    def get_queryset(self):
        """ QuerySet всех индексируемых документов """
        return self.model.objects.all()

    def document_dict(self, instance):
        """ Должен вернуть словарь данных документа, в соответствии со схемой """
        raise NotImplementedError

    def build_xml(self):
        """ Генератор документов """
        yield """<?xml version="1.0" encoding="utf-8"?><sphinx:docset xmlns:sphinx="http://sphinxsearch.com/">"""

        yield from self.build_schema()

        for instance in self.get_queryset():
            output = """<sphinx:document id="{0}">""".format(instance.id)
            for key, value in self.document_dict(instance).items():
                output += """<{0}>{1}</{0}>""".format(
                    key, escape(value) or ''
                )
            output += """</sphinx:document>"""
            yield output

        yield """</sphinx:docset>"""
