"""
    Модуль, предоставляющий базовые методы и классы для
    работы с вариациями картинок
"""

from .croparea import CropArea
from .fields import VariationImageFieldFile, VariationImageField
from .utils import (is_size, check_variations, format_variations, format_aspects, put_on_bg,
                    limited_size, variation_crop, variation_resize, variation_watermark,
                    variation_overlay, variation_mask)

__all__ = ['VariationImageFieldFile', 'VariationImageField', 'CropArea',
           'is_size', 'check_variations', 'format_variations', 'format_aspects', 'put_on_bg',
           'limited_size', 'variation_crop', 'variation_resize', 'variation_watermark',
           'variation_overlay', 'variation_mask']