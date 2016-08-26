def get_paginator_meta(paginator):
    """
        Получение метаданных из постраничной навигации для SEO.

        <link rel="canonical">
        <link rel="next">,
        <link rel="prev">

        Пример:
            # views.py:
                paginator = Paginator(...)

                seo = Seo()
                seo.set(get_paginator_meta(paginator))
    """
    meta = {}

    canonical = paginator.link_to(paginator.current_page_number, anchor=False)
    canonical_absolute_uri = paginator.request.build_absolute_uri(canonical)
    meta['canonical'] = canonical_absolute_uri

    if paginator.previous_page_number:
        prev_page = paginator.link_to(paginator.previous_page_number, anchor=False)
        prev_absolute_uri = paginator.request.build_absolute_uri(prev_page)
        meta['prev'] = prev_absolute_uri

    if paginator.next_page_number:
        next_page = paginator.link_to(paginator.next_page_number, anchor=False)
        next_absolute_uri = paginator.request.build_absolute_uri(next_page)
        meta['next'] = next_absolute_uri

    return meta
