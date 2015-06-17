import operator
import itertools
from PIL import Image, ImageOps, ImageEnhance
from django.contrib.staticfiles import finders


# Действия при несовпадении размера
ACTION_CROP = 1
ACTION_CROP_ANYWAY = 2
ACTION_STRETCH_BY_WIDTH = 3
ACTION_INSCRIBE = 4
ACTIONS = (ACTION_CROP, ACTION_STRETCH_BY_WIDTH, ACTION_CROP_ANYWAY, ACTION_INSCRIBE)


DEFAULT_VARIATION = dict(
    # Размер
    size=(),

    # Тактика при несовпадении размера:
    #   ACTION_CROP:
    #       а) Картинка больше - уменьшить до нужного размера по одной из сторон и обрезать излишки
    #       б) Картинка меньше - сохранить оригинал
    #   ACTION_STRETCH_BY_WIDTH:
    #       Растянуть картинку по ширине, оставив высоту пропорциональной.
    #       Высота в параметре size игнорируется.
    #   ACTION_CROP_ANYWAY:
    #       а) Картинка больше - уменьшить до нужного размера по одной из сторон и обрезать излишки
    #       б) Картинка меньше - растянуть и обрезать
    #   ACTION_INSCRIBE:
    #       а) Картинка больше - уменьшить до нужного размера по одной из сторон
    #       б) Картинка меньше - сохранить оригинал
    #       Создается фон нужного размера, в центр которого вписывается картинка
    action=ACTION_CROP,

    # Положение картинки относительно фона
    position=(0.5, 0.5),

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

    # Использовать для нарезки исходную картинку (игнорирование кропа админки)
    use_source=False,

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
            errors.append(checks.Error('size of variation %r should be a tuple of 2 non-negative numbers' % name, obj=obj))

        # action
        if 'action' not in params:
            errors.append(checks.Error('variation %r requires \'action\' value' % name, obj=obj))
        if params['action'] not in ACTIONS:
            errors.append(checks.Error('unknown action of variation %r' % name, obj=obj))

        # position
        if 'position' in params:
            if not isinstance(params['position'], (list, tuple)):
                errors.append(checks.Error('position of variation %r should be a tuple or list' % name, obj=obj))

        # format
        if params['format']:
            fmt = str(params['format']).upper()
            if fmt not in ('JPG', 'JPEG', 'PNG'):
                errors.append(checks.Error('unacceptable format of variation %r: %r. Allowed types: jpg, jpeg, png' % (name, fmt), obj=obj))

        # overlay
        if params['overlay']:
            overlay_path = finders.find(params['overlay'])
            if not overlay_path:
                errors.append(checks.Error('overlay file not found: %r' % params['overlay'], obj=obj))

        # mask
        if params['mask']:
            mask_path = finders.find(params['mask'])
            if not mask_path:
                errors.append(checks.Error('mask file not found: %r' % params['mask'], obj=obj))

        if params['watermark']:
            watermark = dict(DEFAULT_WATERMARK, **params['watermark'])

            if not isinstance(watermark, dict):
                errors.append(checks.Error('watermark settings should be a dict', obj=obj))

            # file
            if 'file' not in watermark:
                errors.append(checks.Error('watermark file required for variation %r' % name, obj=obj))
            if not finders.find(watermark['file']):
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


def format_variations(variations):
    """ Проверка и форматирование вариаций """
    result = {}
    for name, params in variations.items():
        if isinstance(params, tuple):
            params = {
                'size': params,
            }

        final_params = dict(DEFAULT_VARIATION, name=name, **params)

        # Проверка формата
        image_format = final_params.get('format')
        if image_format:
            image_format = str(image_format).upper()
            if image_format in ('JPG', 'JPEG'):
                image_format = 'JPEG'
        elif final_params.get('mask'):
            # Не указан формат, но указана маска - переводим в PNG
            image_format = 'PNG'
        final_params['format'] = image_format

        # Overlay
        if final_params['overlay']:
            final_params['overlay'] = finders.find(final_params['overlay'])

        # Mask
        if final_params['mask']:
            final_params['mask'] = finders.find(final_params['mask'])

        # Водяной знак
        if final_params['watermark']:
            watermark = dict(DEFAULT_WATERMARK, **final_params['watermark'])
            watermark['file'] = finders.find(watermark['file'])
            watermark['padding'] = tuple(map(int, watermark['padding']))
            watermark['opacity'] = float(watermark['opacity'])
            watermark['scale'] = float(watermark['scale'])
            watermark['position'] = str(watermark['position']).upper()
            final_params['watermark'] = watermark

        result[name] = final_params

    return result


def format_aspects(value, variations):
    """ Форматирование аспектов """
    result = []
    aspects = value if isinstance(value, tuple) else (value, )
    for aspect in aspects:
        try:
            aspect = float(aspect)
        except (TypeError, ValueError):
            if aspect in variations:
                aspect = operator.truediv(*variations[aspect]['size'])
            else:
                continue
        result.append(str(round(aspect, 4)))
    return tuple(result)


def put_on_bg(image, bg_size, bg_color, position, masked=False):
    """ Создание фона цветом bg_color и размера bg_size, на который будет наложена картинка image """
    background = Image.new('RGBA', bg_size, bg_color)
    size_diff = list(itertools.starmap(operator.sub, zip(background.size, image.size)))
    offset = (int(size_diff[0] * position[0]), int(size_diff[1] * position[1]))
    if masked:
        background.paste(image, offset, image)
    else:
        background.paste(image, offset)
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


def variation_crop(image, crop=None):
    """ Обрезка по координатам """
    if not crop:
        return image

    left, top, width, height = crop
    if left < 0:
        left = 0
    if left + width > image.size[0]:
        width = image.size[0] - left

    if top < 0:
        top = 0
    if top + height > image.size[1]:
        height = image.size[1] - top

    return image.crop((
        left,
        top,
        left + width,
        top + height))


def variation_resize(image, variation, target_format):
    """
        Изменение размера в соответствии с variation[action] и variation[size]
    """
    target_bgcolor = variation['background']

    # Целевой размер
    target_size = variation['size']
    if not isinstance(target_size, (list, tuple)) or len(target_size) != 2:
        raise ValueError('Invalid image size: %r' % target_size)

    # Отношение площадей исходника и вариации
    relation = min(itertools.starmap(operator.truediv, zip(image.size, target_size)))
    relation /= 4
    if relation > 1:
        middle_size = tuple(int(p/relation) for p in image.size)
        image = image.resize(middle_size, Image.NEAREST)

    # Действие при несовпадении размера
    target_action = variation['action']
    target_position = variation['position']
    if target_action == ACTION_CROP:
        if image.size[0] < target_size[0] and image.size[1] < target_size[1]:
            # Если картинка меньше - оставляем её как есть
            pass
        elif image.size[0] < target_size[0] or image.size[1] < target_size[1]:
            # Если она меньше по одной стороне - отрезаем излишки у другой
            image.thumbnail(target_size, resample=Image.ANTIALIAS)
        else:
            image = ImageOps.fit(image, target_size, method=Image.ANTIALIAS)

        # При сохранении PNG/GIF в JPEG прозрачный фон становится черным. Накладываем на фон
        if image.mode == 'RGBA' and target_format=='JPEG':
            image = put_on_bg(image, image.size, target_bgcolor, target_position, masked=True)
    elif target_action == ACTION_CROP_ANYWAY:
        image = ImageOps.fit(image, target_size, method=Image.ANTIALIAS)

        # При сохранении PNG/GIF в JPEG прозрачный фон становится черным. Накладываем на фон
        if image.mode == 'RGBA' and target_format=='JPEG':
            image = put_on_bg(image, image.size, target_bgcolor, target_position, masked=True)
    elif target_action == ACTION_STRETCH_BY_WIDTH:
        img_aspect = operator.truediv(*image.size)

        final_size = (target_size[0], round(target_size[0] / img_aspect))
        image = ImageOps.fit(image, final_size, method=Image.ANTIALIAS)

        # При сохранении PNG/GIF в JPEG прозрачный фон становится черным. Накладываем на фон
        if image.mode == 'RGBA' and target_format=='JPEG':
            image = put_on_bg(image, final_size, target_bgcolor, target_position, masked=True)
    elif target_action == ACTION_INSCRIBE:
        image.thumbnail(target_size, resample=Image.ANTIALIAS)

        # Наложение с маской для формата PNG вызывает потерю качества
        masked = image.mode == 'RGBA' and target_format != 'PNG'
        image = put_on_bg(image, target_size, target_bgcolor, target_position, masked=masked)

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
