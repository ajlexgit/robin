import operator
import itertools
from PIL import Image, ImageOps, ImageEnhance
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage
from .croparea import CropArea
from .size import Size


DEFAULT_VARIATION = dict(
    # Размер
    size=(),

    stretch=False,
    crop=True,

    # Максимальные размеры результата.
    # Используется только при crop=False
    max_width = 0,
    max_height = 0,

    # Положение картинки относительно фона, если производится наложение.
    # offset - отношение разницы размеров по горизонтали и вертикали.
    # center - относительное положение центра накладываемой картинки.
    # Можно указать только один из параметров offset/center.
    offset=(0.5, 0.5),
    center=(0.5, 0.5),

    # Цвет фона, на который накладывается изображение, когда оно не может сохранить прозрачность
    background=(255, 255, 255, 0),

    # Файл-маска для обрезания картинки
    mask=None,

    # Файл, накладываемый на картинку
    overlay=None,

    # Настройки наложения водяного знака.
    # Например:
    #   watermark = {
    #       file: 'img/watermark.png',
    #       position: 'BR',
    #       padding: (20, 30),
    #       opacity: 1,
    #       scale: 1,
    #   }
    watermark=None,

    # Требуемый формат изображения (JPEG/PNG/GIF)
    format=None,

    # Сохранить EXIF
    exif=False,

    # Качество результата картинки (0-100)
    quality=None,
)


DEFAULT_WATERMARK = {
    'file': '',
    'position': 'BR',
    'padding': (0, 0),
    'opacity': 1,
    'scale': 1,
}


def is_size(value):
    """ Проверка, что value - это кортеж из двух неотрицательных чисел """
    if not isinstance(value, tuple):
        return False
    elif len(value) != 2:
        return False

    try:
        return all(int(item) >= 0 for item in value)
    except (TypeError, ValueError):
        return False


def split_every(n, iterable):
    i = iter(iterable)
    piece = list(itertools.islice(i, n))
    while piece:
        yield piece
        piece = list(itertools.islice(i, n))


def calculateHash(image, hash_size=12):
    """
        Рассчет хэша картинки
    """
    if hash_size ** 2 % 8:
        raise ValueError('"size**2" must be divisible by 8')

    image.seek(0)

    # Grayscale and shrink
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS
    )

    # Compare adjacent pixels
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    hex_string = []
    for bin_array in split_every(8, difference):
        hex_string.append(
            '{0:02x}'.format(int(''.join(str(int(_)) for _ in bin_array), 2))
        )

    return ''.join(hex_string)


def check_variations(variations, obj):
    from django.core import checks
    errors = []

    for name, params in variations.items():
        if isinstance(params, tuple):
            params = {
                'size': params,
            }

        params = dict(DEFAULT_VARIATION, **params)

        if not isinstance(params, dict):
            errors.append(checks.Error('variation %r should be a dict or tuple' % name, obj=obj))

        if not params:
            errors.append(checks.Error('variation %r is empty' % name, obj=obj))

        # size
        if 'size' not in params:
            errors.append(checks.Error('variation %r requires \'size\' value' % name, obj=obj))
        if not is_size(params['size']):
            errors.append(checks.Error('"size" in variation %r should be a tuple of 2 non-negative numbers' % name, obj=obj))

        # crop
        if not isinstance(params['crop'], bool):
            errors.append(checks.Error('"crop" in variation %r must be a boolean' % name, obj=obj))

        # stretch
        if not isinstance(params['stretch'], bool):
            errors.append(checks.Error('"stretch" in variation %r must be a boolean' % name, obj=obj))

        # max_width and max_height
        if not isinstance(params['max_width'], int) or params['max_width'] < 0:
            errors.append(checks.Error('"max_width" in variation %r must be a non-negative integer' % name, obj=obj))
        if not isinstance(params['max_height'], int) or params['max_height'] < 0:
            errors.append(checks.Error('"max_height" in variation %r must be a non-negative integer' % name, obj=obj))
        if params['crop'] and (params['max_width'] or params['max_height']):
            errors.append(checks.Error('"max_width" and "max_height" allowed only when crop=False in variation %r' % name, obj=obj))

        if not any(d for d in params['size']) and not params['max_width'] and not params['max_height']:
            errors.append(checks.Error('"size" in variation %r is empty and non-calulatable' % name, obj=obj))

        # offset
        if 'offset' in params:
            if params['offset'] and not isinstance(params['offset'], (list, tuple)):
                errors.append(checks.Error('"offset" in variation %r should be a tuple or list' % name, obj=obj))

        # center
        if 'center' in params:
            if params['center'] and not isinstance(params['center'], (list, tuple)):
                errors.append(checks.Error('"center" in variation %r should be a tuple or list' % name, obj=obj))

        # format
        if params['format']:
            fmt = str(params['format']).upper()
            if fmt not in ('JPG', 'JPEG', 'PNG'):
                errors.append(checks.Error('unacceptable format of variation %r: %r. Allowed types: jpg, jpeg, png' % (name, fmt), obj=obj))

        # overlay
        if params['overlay'] and not find(params['overlay']):
            errors.append(checks.Error('overlay file not found: %r' % params['overlay'], obj=obj))

        # mask
        if params['mask'] and not find(params['mask']):
            errors.append(checks.Error('mask file not found: %r' % params['mask'], obj=obj))

        if params['watermark']:
            watermark = dict(DEFAULT_WATERMARK, **params['watermark'])

            if not isinstance(watermark, dict):
                errors.append(checks.Error('watermark settings should be a dict', obj=obj))

            # file
            if 'file' not in watermark:
                errors.append(checks.Error('watermark file required for variation %r' % name, obj=obj))
            if not find(watermark['file']):
                errors.append(checks.Error('watermark file not found: %r' % watermark['file'], obj=obj))

            # padding
            if not isinstance(watermark['padding'], (list, tuple)):
                errors.append(checks.Error('watermark\'s padding should be a tuple or list', obj=obj))
            try:
                watermark['padding'] = tuple(map(int, watermark['padding']))
            except (ValueError, TypeError):
                errors.append(checks.Error('invalid watermark padding: %r' % watermark['padding'], obj=obj))

            # opacity
            try:
                watermark['opacity'] = float(watermark['opacity'])
            except (TypeError, ValueError):
                errors.append(checks.Error('watermark\'s opacity should be a float', obj=obj))
            else:
                if watermark['opacity'] < 0 or watermark['opacity'] > 1:
                    errors.append(checks.Error('watermark\'s opacity should be in interval [0, 1]', obj=obj))

            # scale
            try:
                watermark['scale'] = float(watermark['scale'])
            except (TypeError, ValueError):
                errors.append(checks.Error('watermark\'s scale should be a float', obj=obj))
            else:
                if watermark['scale'] <= 0:
                    errors.append(checks.Error('watermark\'s scale should be greater than 0', obj=obj))

            # position
            watermark['position'] = str(watermark['position']).upper()
            if watermark['position'] not in ('TL', 'TR', 'BL', 'BR', 'C'):
                errors.append(checks.Error('watermark\'s position should be in (TL, TR, BL, BR, C)', obj=obj))

    return errors


def format_variation(**params):
    """
        Приведение настроек вариации к каноническому виду
    """
    variation = dict(DEFAULT_VARIATION, **params)

    # Проверка формата
    image_format = variation.get('format')
    if image_format:
        image_format = str(image_format).upper()
        if image_format in ('JPG', 'JPEG'):
            image_format = 'JPEG'
    elif variation.get('mask'):
        # Не указан формат, но указана маска - переводим в PNG
        image_format = 'PNG'
    variation['format'] = image_format

    # Overlay
    overlay = variation.get('overlay')
    if overlay:
        variation['overlay'] = staticfiles_storage.path(overlay)

    # Mask
    mask = variation.get('mask')
    if mask:
        variation['mask'] = staticfiles_storage.path(mask)

    # Водяной знак
    watermark = variation.get('watermark')
    if watermark and isinstance(watermark, dict):
        watermark = dict(DEFAULT_WATERMARK, **watermark)
        watermark['file'] = staticfiles_storage.path(watermark['file'])
        watermark['padding'] = tuple(map(int, watermark['padding']))
        watermark['opacity'] = float(watermark['opacity'])
        watermark['scale'] = float(watermark['scale'])
        watermark['position'] = str(watermark['position']).upper()
        variation['watermark'] = watermark

    return variation


def format_variations(variations):
    """ Форматирование вариаций """
    return {
        name: dict(format_variation(**params), name=name)
        for name, params in variations.items()
    }


def format_aspects(value, variations):
    """ Форматирование аспектов """
    result = []
    aspects = value if isinstance(value, tuple) else (value, )
    for aspect in aspects:
        try:
            aspect = float(aspect)
        except (TypeError, ValueError):
            if aspect not in variations:
                continue

            size = variations[aspect]['size']
            if all(d > 0 for d in size):
                aspect = operator.truediv(*size)
            else:
                continue

        result.append(str(round(aspect, 4)))
    return tuple(result)


def put_on_bg(image, bg_size, color=(255,255,255,0), offset=(0.5, 0.5), center=(0.5, 0.5), masked=False):
    """ Создание фона цветом bg_color и размера bg_size, на который будет наложена картинка image """
    background = Image.new('RGBA', bg_size, color)

    if center:
        final_offset = (
            max(0, int(background.size[0] * center[0] - image.size[0] / 2)),
            max(0, int(background.size[1] * center[1] - image.size[1] / 2))
        )
    else:
        size_diff = list(itertools.starmap(operator.sub, zip(background.size, image.size)))
        final_offset = (int(size_diff[0] * offset[0]), int(size_diff[1] * offset[1]))

    if masked:
        try:
            background.paste(image, final_offset, image)
        except ValueError:
            background.paste(image, final_offset)
    else:
        background.paste(image, final_offset)
    return background


def limited_size(size, limit_size):
    """
        Пропорциональное уменьшение размера size, чтобы он не превосходил limit_size.
        Допустимо частичное указание limit_size, например, (1024, 0).
        Если size умещается в limit_size, возвращает None
    """
    max_width, max_height = limit_size
    if not max_width and not max_height:
        return None

    width, height = size
    if max_width and width > max_width:
        height = height * (max_width / width)
        width = max_width
    if max_height and height > max_height:
        width = width * (max_height / height)
        height = max_height
    width, height = round(width), round(height)
    if size == (width, height):
        return None

    return width, height


def variation_crop(image, croparea=None):
    """ Обрезка по координатам """
    if not croparea:
        return image

    if not isinstance(croparea, CropArea):
        croparea = CropArea(croparea)

    if croparea.x2 > image.size[0]:
        croparea.width = image.size[0] - croparea.x

    if croparea.y2 > image.size[1]:
        croparea.height = image.size[1] - croparea.y

    cropped = image.crop((
        croparea.x,
        croparea.y,
        croparea.x2,
        croparea.y2
    ))
    cropped.format = image.format
    return cropped


def variation_resize(image, variation, target_format):
    """
        Изменение размера
    """
    bg_options = {
        'color': variation['background'],
        'offset': variation['offset'],
        'center': variation['center'],
    }

    # Целевой размер
    target_size = variation['size']
    if not isinstance(target_size, (list, tuple)) or len(target_size) != 2:
        raise ValueError('Invalid image size: %r' % target_size)

    # Режим изображения
    mode = image.mode
    image_format = image.format
    crop = bool(variation['crop'])
    stretch = bool(variation['stretch'])

    source_size = image.size
    need_bg = bg_options['color'][3] != 0 or mode == 'RGBA' or target_format == 'JPEG'

    if crop:
        # Быстрое уменьшение картинки, если целевой размер намного меньше
        if not target_size[0]:
            target_size = (source_size[0], target_size[1])
        elif not target_size[1]:
            target_size = (target_size[0], source_size[1])

        if stretch:
            # OLD: CROP_ANYWAY
            image = ImageOps.fit(image, target_size, method=Image.ANTIALIAS, centering=bg_options['center'])
        else:
            # OLD: CROP
            new_width = min(source_size[0], target_size[0])
            new_height = min(source_size[1], target_size[1])
            if new_width == source_size[0] and new_height == source_size[1]:
                # Если целевой размер больше - оставляем картинку без изменений
                pass
            else:
                image = ImageOps.fit(image, (new_width, new_height), method=Image.ANTIALIAS, centering=bg_options['center'])
    else:
        # Размеры картинки, вписываемой в холст
        image_size = Size(*source_size)

        max_width = variation['max_width']
        max_height = variation['max_height']

        # корректируем ограничения
        max_width = min(max_width or target_size[0], target_size[0] or max_width)
        max_height = min(max_height or target_size[1], target_size[1] or max_height)

        # Определяем размеры картинки
        if stretch:
            # растягивать разрешено
            if max_width:
                if max_height:
                    max_aspect = max_width / max_height
                    if image_size.aspect > max_aspect:
                        # картинка шире холста
                        image_size.width = max_width
                    else:
                        # картинка выше холста
                        image_size.height = max_height
                else:
                    # плавающая выcота
                    image_size.width = max_width
            else:
                if max_height:
                    # плавающая ширина
                    image_size.height = max_height
        else:
            # растягивать запрещено
            if max_width:
                image_size.max_width(max_width)
            if max_height:
                image_size.max_height(max_height)

        # если размер вычисляется автоматически и нет прозрачности - накладывать на фон не нужно
        need_bg = need_bg or target_size != (0, 0)

        # Определение размера холста
        target_size = list(target_size)
        if target_size[0] == 0:
            target_size[0] = image_size.width
        if target_size[1] == 0:
            target_size[1] = image_size.height

        # Ресайз
        img_size = (image_size.width, image_size.height)
        if stretch:
            image = image.resize(img_size, resample=Image.ANTIALIAS)
        else:
            # OLD: INSRIBE
            image.thumbnail(img_size, resample=Image.ANTIALIAS)


    # Накладываем на фон
    if need_bg:
        masked = bg_options['color'][3] != 0  # баг потери качества PNG при наложении
        image = put_on_bg(image, target_size, masked=masked, **bg_options)

    image.format = image_format
    return image


def variation_watermark(image, variation):
    """ Наложение водяного знака на картинку """
    wm_settings = variation['watermark']
    if not wm_settings:
        return image

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    with open(wm_settings['file'], 'rb') as fp:
        watermark = Image.open(fp)
        info = watermark.info
        if watermark.mode not in ('RGBA', 'LA') and not (watermark.mode == 'P' and 'transparency' in info):
            watermark.putalpha(255)

        img_width, img_height = image.size
        wm_width, wm_height = watermark.size

        scale = wm_settings['scale']
        if scale != 1:
            watermark = watermark.resize((int(wm_width*scale), int(wm_height*scale)), Image.ANTIALIAS)
            wm_width, wm_height = watermark.size

        position = wm_settings['position']
        padding = wm_settings['padding']
        if position == 'TL':
            left = padding[0]
            top = padding[1]
        elif position == 'TR':
            left = img_width - wm_width - padding[0]
            top = padding[1]
        elif position == 'BL':
            left = padding[0]
            top = img_height - wm_height - padding[1]
        elif position == 'BR':
            left = img_width - wm_width - padding[0]
            top = img_height - wm_height - padding[1]
        elif position == 'C':
            top = (img_height - wm_height) // 2
            left = (img_width - wm_width) // 2
        else:
            left = top = padding

        opacity = wm_settings['opacity']
        if opacity < 1:
            alpha = watermark.convert('RGBA').split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
        image.paste(watermark, (left, top), watermark)

    return image


def variation_overlay(image, variation):
    """ Наложение оверлея на картинку """
    overlay = variation['overlay']
    if not overlay:
        return image

    overlay_img = Image.open(overlay)
    if overlay_img.size != image.size:
        overlay_img = ImageOps.fit(overlay_img, image.size, method=Image.ANTIALIAS)

    # Дикие баги картинки, когда GIF => PNG + overlay
    if image.mode == 'P':
        image = image.convert('RGBA')

    image.paste(overlay_img, overlay_img)

    return image


def variation_mask(image, variation):
    """ Обрезка картинки по маске """
    target_bgcolor = variation['background']

    mask = variation['mask']
    if not mask:
        return image

    mask_img = Image.open(mask).convert('L')
    if mask_img.size != image.size:
        mask_img = ImageOps.fit(mask_img, image.size, method=Image.ANTIALIAS)

    background = Image.new("RGBA", image.size, target_bgcolor)
    image = Image.composite(image, background, mask_img)

    return image


def process_variation(source, variation, quality=None, croparea=None):
    """ Обработка картинки в соответствии с вариацией """
    with open(source, 'rb') as fp:
        image = Image.open(fp)
        image.load()

    # Параметры сохранения
    image_info = {}
    if variation['exif']:
        image_info.update(image.info or {})

    # Обрезаем по рамке
    if croparea is not None:
        image = variation_crop(image, croparea)

    # Целевой формат
    target_format = variation['format'] or image.format
    target_format = target_format.upper()

    # Параметры сохранения
    image_info.update(
        format=target_format,
        quality=quality or variation.get('quality'),
    )

    # Изображение с режимом "P" нельзя сохранять в JPEG,
    # а в GIF - фон становится черным
    if image.mode == 'P' and target_format in ('JPEG', 'GIF'):
        image = image.convert('RGBA')

    # При сохранении в GIF проблематично указать прозрачность. Кроме того,
    # Уменьшенный в размере прозрачный GIF ужасен по качеству. Пока накладываем на фон
    if target_format == 'GIF':
        masked = image.mode == 'RGBA'
        image = put_on_bg(image, image.size,
            color=variation['background'][:3],
            offset=variation['offset'],
            masked=masked)

    # Основная обработка картинок
    image = variation_resize(image, variation, target_format)
    image = variation_watermark(image, variation)
    image = variation_overlay(image, variation)
    image = variation_mask(image, variation)
    return image, image_info


def process_image(source, croparea=None, **params):
    """ Алиас для тестов. Обработка картинки в соответствии с вариацией """
    variation = format_variation(**params)
    return process_variation(source, variation, croparea=croparea)
