from libs.async_block import AsyncBlockView


class AsyncHeader(AsyncBlockView):
    """ Пример асинхронного блока """
    allowed= ('id', )
    
    def render(self, request, id=''):
        return '(ID %s)' % id