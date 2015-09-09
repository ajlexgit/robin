"""
    Обертка над постраничной навигацией.

    Пример использования:
        # views.py
            from paginator import Paginator, EmptyPage

            ...
            try:
                paginator = Paginator(request,
                    object_list=Post.objects.all(),
                    per_page=5,
                    allow_empty_first_page=False,
                )
            except EmptyPage:
                raise Http404
            ...

        # template.html
            <!-- Элементы текущей страницы -->
            {% for item in paginator.page %}
                {{ item.name }}
                ...
            {% endfor %}

            <!-- Навигация -->
            {% if paginator.num_pages > 1 %}
                <div class="grid">
                    <div class="gc-wide-6 gc-6 gc-tablet-6 gc-mobile-4 gc-alone">
                        {{ paginator }}
                    </div>
                </div>
            {% endif %}


    По умолчанию реализует постраничную навигацию через
    GET-параметр Paginator.parameter_name.

    Свойство Paginator.zipped_page_range возвращает список
    номеров страниц, длинные промежутки в которых заменены на None,
    который в шаблоне заменяется на многоточие.
    Настройка сжимаемого диапазона осуществляется через
    Paginator.page_neighbors и Paginator.min_zip_pages.

        Paginator.page_neighbors - количество страниц, соседних
        с текущей с каждой стороны, чьи номера будут показаны.

        Paginator.side_neighbors - количество страниц, соседних
        с граничными, чьи номера будут показаны.

        Paginator.min_zip_pages - минимальное количествово страниц,
        заменямых на None.

    Примеры:
        1) page_neighbors = 2, side_neighbors = 0, min_zip_pages = 2
            (1) 2 3 ... 10
            1 2 (3) 4 5 ... 10
            1 ... 5 6 (7) 8 9 10
            1 ... 7 8 (9) 10

        2) page_neighbors = 2, side_neighbors = 2, min_zip_pages = 2
            (1) 2 3 ... 8 9 10
            1 2 (3) 4 5 ... 8 9 10
            1 2 3 4 5 6 (7) 8 9 10
            1 2 3 ... 6 7 (8) 9 10

        3) page_neighbors = 0, side_neighbors = 0, min_zip_pages = 2
            (1) ... 10
            1 2 (3) ... 10
            1 ... (5) ... 10
            1 ... (8) 9 10

    Для реализации постраничной навигации, при которой все
    страницы изначально находятся на странице и навигация
    осуществляется через показ/скрытие контейнеров через JS - добавлено
    свойство Paginator.pages, возвращающее кортеж объектов Paginator.Page.

"""

from .paginator import Paginator, EmptyPage
