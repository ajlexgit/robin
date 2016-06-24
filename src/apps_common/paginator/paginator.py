from django.template import loader
from django.core import paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils.functional import cached_property


class Paginator(paginator.Paginator):
    parameter_name = 'page'
    template = 'paginator/paginator.html'

    def __init__(self, request, *args, **kwargs):
        # При сжатии страниц: кол-во страниц, соседних текущей с каждой стороны,
        # чьи номера будут показаны
        self.page_neighbors = kwargs.pop('page_neighbors', 2)

        # При сжатии страниц: кол-во страниц, соседних с граничными,
        # чьи номера будут показаны
        self.side_neighbors = kwargs.pop('side_neighbors', 0)

        # При сжатии страниц: минимальное кол-во страниц, заменямых многоточием
        self.min_zip_pages = kwargs.pop('min_zip_pages', 2)

        # Якорь, добавляемяй к ссылкам
        self.anchor = kwargs.pop('anchor', '')

        super().__init__(*args, **kwargs)
        self.request = request
        if not self.allow_empty_first_page and self.count == 0:
            raise EmptyPage('That page contains no results')

    def real_page_number(self, number):
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            return 1
        except EmptyPage:
            return self.num_pages
        else:
            return number

    @cached_property
    def current_page(self):
        """ Объект текущей страницы """
        new_number = self.request.GET.get(self.parameter_name, 1)
        new_number = self.real_page_number(new_number)
        return self.page(new_number)

    @cached_property
    def pages(self):
        """ Кортеж всех объектов страниц с их полными данными """
        self.object_list = self.object_list[:]      # принудительное выполнение запроса
        return tuple((page_num, self.page(page_num)) for page_num in self.num_pages)

    @cached_property
    def zipped_page_range(self):
        """ Список номеров страниц с учетом сокращения длинного списка """
        left_page = max(1, self.current_page.number - self.page_neighbors)
        right_page = min(self.num_pages, self.current_page.number + self.page_neighbors)
        result = []

        if left_page > 1 + self.side_neighbors + self.min_zip_pages:
            result += list(range(1, 2 + self.side_neighbors)) + [None] + list(range(left_page, right_page + 1))
        else:
            result += list(range(1, right_page + 1))

        if right_page < self.num_pages - self.side_neighbors - self.min_zip_pages:
            result += [None] + list(range(self.num_pages - self.side_neighbors, self.num_pages + 1))
        else:
            result += list(range(right_page + 1, self.num_pages + 1))

        return result

    def href(self, number):
        """ Построение ссылки на страницу с номером number """
        if number == 1:
            return '?'
        else:
            return '?%s=%s' % (self.parameter_name, number)

    def __str__(self):
        if not self.current_page.has_other_pages():
            return ''

        return loader.render_to_string(self.template, {
            'paginator': self,
            'page': self.current_page,
            'anchor': self.anchor,
        })
