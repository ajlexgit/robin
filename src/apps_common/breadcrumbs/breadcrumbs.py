class Breadcrumbs:
    def __init__(self):
        self.crumbs = []

    def __bool__(self):
        return bool(self.crumbs)

    def __iter__(self):
        return iter(self.crumbs)

    def add(self, title, url='', **kwargs):
        self.crumbs.append(dict(
            title=title,
            url=url,
            **kwargs
        ))
