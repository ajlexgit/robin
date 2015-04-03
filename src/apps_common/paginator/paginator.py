from django.template import loader
from django.core import paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils.functional import cached_property


class Paginator(paginator.Paginator):
    parameter_name = 'page'
    template = 'paginator/paginator.html'
    
    # При сжатии страниц: кол-во страниц, соседних текущей с каждой стороны,
    # чьи номера будут показаны
    page_neighbors = 2
    
    # При сжатии страниц: минимальное кол-во страниц, заменямых многоточием
    min_zip_pages = 2
    
    def __init__(self, request, *args, **kwargs):
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
    def page(self):
        """ Объект текущей страницы """
        number = self.request.GET.get(self.parameter_name)
        number = self.real_page_number(number)
        return super().page(number)
    
    @cached_property
    def pages(self):
        """ Кортеж всех объектов страниц с их полными данными """
        self.object_list = self.object_list[:]      # принудительное выполнение запроса
        return ( super().page(page_num) for page_num in self.num_pages )
    
    @cached_property
    def zipped_page_range(self):
        """ Список номеров страниц с учетом сокращения длинного списка """
        page = self.page
        left_page = max(1, page.number - self.page_neighbors)
        right_page = min(self.num_pages, page.number + self.page_neighbors)
        result = []
        
        if left_page > 1 + self.page_neighbors + self.min_zip_pages:
            result += list(range(1, 2 + self.page_neighbors)) + [None] + list(range(left_page, right_page + 1))
        else:
            result += list(range(1, right_page + 1))
        
        if right_page < self.num_pages - self.page_neighbors - self.min_zip_pages:
            result += [None] + list(range(self.num_pages - self.page_neighbors, self.num_pages + 1))
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
        page = self.page
        if not page.has_other_pages():
            return ''
            
        return loader.render_to_string(self.template, {
            'paginator': self,
            'page': page,
        })
    
    