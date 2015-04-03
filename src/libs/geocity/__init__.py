from . import options
from pysyge.pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY

geodata = GeoLocator(options.DB_PATH, MODE_BATCH | MODE_MEMORY)

def info(ip, detailed=False):
    """ 
        Получение информации о IP.
        
        Пример:
            >>> info('8.8.8.8')
            {'region': None,
             'country': {'lon': -98.5,
              'iso': 'US',
              'lat': 39.76,
              'name_en': 'United States',
              'name_ru': 'США',
              'id': 225},
             'city': {'lat': 39.76,
              'name_en': True,
              'lon': -98.5,
              'name_ru': True,
              'id': 0}}
            
    """
    data = geodata.get_location(ip, detailed)
    return data.get('info') if data else data

__all__ = ['info']