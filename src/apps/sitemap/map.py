class Map:
    __slots__ = ('childs', )

    def __init__(self):
        self.childs = []

    def __iter__(self):
        return iter(self.childs)

    def add_child(self, instance):
        """ Добавление одной сущности """
        record = MapRecord(instance)
        self.childs.append(record)
        return record

    def add_childs(self, queryset):
        """ Добавление всех сущностей из QuerySet """
        records = tuple(MapRecord(instance) for instance in queryset)
        self.childs.extend(records)
        return records


class MapRecord(Map):
    __slots__ = ('title', 'url', 'childs')

    def __init__(self, instance):
        self.title = str(instance)
        self.url = instance.get_absolute_url()
        super().__init__()
