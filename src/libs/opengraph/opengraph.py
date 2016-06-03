from django.template import loader


class Opengraph(dict):
    OG_PREFIXED = ('url', 'title', 'image', 'description', 'type')

    def render(self):
        params = {
            'og:type': 'website',
        }
        for key, value in self.items():
            value = str(value).strip()
            if value:
                if key in self.OG_PREFIXED:
                    params['og:%s' % key] = value
                else:
                    params[key] = value

        return loader.render_to_string('opengraph/opengraph.html', {
            'params': params,
        })


class TwitterCard(dict):
    FROM_OPENGRAPH = ('title', 'description', 'image')

    def render(self):
        params = {
            'card': 'summary',
        }
        for key, value in self.items():
            value = str(value).strip()
            if value and key in self.FROM_OPENGRAPH:
                params[key] = value

        return loader.render_to_string('opengraph/twitter_card.html', {
            'params': params,
        })
