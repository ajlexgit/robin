import random
from decimal import Decimal
from urllib.request import urlretrieve
from django.apps import apps
from django.core.files import File
from django.db.models import fields
from django.core.management import BaseCommand
from django.utils.text import Truncator, slugify
from django.utils.timezone import now, timedelta
from django.db.models.fields.files import FileField, ImageField
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from ckeditor.fields import CKEditorField, CKEditorUploadField
from libs.stdimage.fields import StdImageField
from ._filldb_private import get_field_choices, generate_random_string, generate_lorem_ipsum


def set_boolean(instance, field):
    """ BooleanField """
    possibles = [True, False]
    possibles.extend(get_field_choices(field))
    setattr(instance, field.name, random.choice(possibles))


def set_chars(instance, field):
    """ CharField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    max_len = field.max_length
    for validator in field.validators:
        if isinstance(validator, MaxLengthValidator):
            max_len = min(max_len, validator.limit_value)

    value = generate_lorem_ipsum(1, min=1, max=max(5, max_len // 8), html=False)
    value = Truncator(value).chars(max_len, html=False)
    setattr(instance, field.name, value)


def set_text(instance, field, paragraphs=1, html=False):
    """ TextField """
    max_len = field.max_length or 16 * 1024
    for validator in field.validators:
        if isinstance(validator, MaxLengthValidator):
            max_len = min(max_len, validator.limit_value)

    value = generate_lorem_ipsum(paragraphs, html=html)
    value = Truncator(value).chars(max_len, html=html)
    setattr(instance, field.name, value)


def set_slug(instance, field):
    """ SlugField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    value = slugify(generate_lorem_ipsum(1, min=1, max=6))
    value = Truncator(value).chars(field.max_length, html=False)
    setattr(instance, field.name, value)


def set_integer(instance, field, min_value=-2**31, max_value=2**31 - 1):
    """ IntegerField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    for validator in field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = max(min_value, validator.limit_value)
        if isinstance(validator, MaxValueValidator):
            max_value = min(max_value, validator.limit_value)

    value = random.randint(min_value, max_value)
    setattr(instance, field.name, value)


def set_date(instance, field):
    """ DateField """
    start = 2 * 24 * 3600
    end = 5 * 365 * 24 * 3600
    value = now() - timedelta(seconds=random.randint(start, end))
    setattr(instance, field.name, value)


def set_decimal(instance, field, max_digits=10):
    """ DecimalField """
    max_digits = min(max_digits, field.max_digits)
    min_value = -10 ** max_digits
    max_value = 10 ** max_digits
    for validator in field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = max(min_value, validator.limit_value)
        if isinstance(validator, MaxValueValidator):
            max_value = min(max_value, validator.limit_value)

    value = random.randint(min_value, max_value)
    value = Decimal(value) / 10 ** field.decimal_places

    setattr(instance, field.name, value)


def set_email(instance, field):
    """ EmailField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    value = generate_random_string(min=2, max=20)
    setattr(instance, field.name, '%s@gmail.com' % value)


def set_float(instance, field):
    """ FloatField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    min_value = -2 ** 8
    max_value = 2 ** 8 - 1
    for validator in field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = max(min_value, validator.limit_value)
        if isinstance(validator, MaxValueValidator):
            max_value = min(max_value, validator.limit_value)

    value = random.uniform(min_value, max_value)
    setattr(instance, field.name, value)


def set_url(instance, field):
    """ URLField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    max_len = field.max_length
    for validator in field.validators:
        if isinstance(validator, MaxLengthValidator):
            max_len = min(max_len, validator.limit_value)

    value = 'http://google.com/%s/' % generate_random_string(5, 10)
    value = Truncator(value).chars(max_len, html=False)
    setattr(instance, field.name, value)


def set_fk(instance, field):
    """ ForeignKey / OneToOneField """
    if field.unique:
        return

    related = field.rel.to.objects.all()
    if not related:
        raise ValueError('no instances for field "%s"' % field.name)

    min_index = 0 if field.null else 1
    max_index = related.count()

    index = random.randint(min_index, max_index)
    if index is 0:
        value = None
    else:
        value = related[index-1]

    setattr(instance, field.name, value)


def set_m2m(instance, field, max_count=4):
    """ ManyToManyField """
    related = field.rel.to.objects.all()
    if not related:
        raise ValueError('no instances for field "%s"' % field.name)

    min_count = 0 if field.blank else 1
    max_count = min(max_count, related.count())

    manager = getattr(instance, field.name)
    for item in related.order_by('?')[:random.randint(min_count, max_count)]:
        manager.add(item)


def set_image(instance, field, width=1920, height=1440):
    """ FileField / ImageField """
    manager = getattr(instance, field.name)
    local_filename, headers = urlretrieve('https://unsplash.it/%d/%d/?random' % (width, height))
    with open(local_filename, 'rb') as img:
        manager.save('image.jpg', File(img), save=False)


def set_stdimage(instance, field):
    """ StdImageField """
    min_width, min_height = field.min_dimensions
    max_width, max_height = field.max_dimensions

    width = min_width if min_width else 1920
    height = min_height if min_height else 1440
    if max_width:
        width = min(width, max_width)
    if max_height:
        height = min(height, max_height)

    set_image(instance, field, width=width, height=height)


class Command(BaseCommand):
    """
        Заполнение БД рандомными данными
    """
    help = 'Fill database with random data'

    def add_arguments(self, parser):
        parser.add_argument(
            action='store',
            dest='model',
            help='Object model (e.g. "news.post")'
        )
        parser.add_argument('-c', '--count',
            action='store',
            dest='count',
            type=int,
            default=1,
            help='Number of objects to create'
        )

    def handle(self, *args, **options):
        try:
            app, model = options['model'].split('.')
        except (ValueError, AttributeError):
            raise ValueError('invalid "model" value')

        Model = apps.get_model(app, model)

        count = options['count']
        if count <= 0:
            raise ValueError('"count" must be greather than 0')

        for _ in range(count):
            print('Creating object %d of %d...' % (_ + 1, count))

            instance = Model()
            for field in Model._meta.get_fields():
                if field.auto_created:
                    continue

                if field.is_relation:
                    if field.many_to_many:
                        continue
                    else:
                        set_fk(instance, field)
                elif isinstance(field, fields.BooleanField):
                    set_boolean(instance, field)
                elif isinstance(field, fields.EmailField):
                    set_email(instance, field)
                elif isinstance(field, fields.SlugField):
                    set_slug(instance, field)
                elif isinstance(field, fields.PositiveSmallIntegerField):
                    set_integer(instance, field, min_value=0, max_value=32767)
                elif isinstance(field, fields.PositiveIntegerField):
                    set_integer(instance, field, min_value=0)
                elif isinstance(field, fields.SmallIntegerField):
                    set_integer(instance, field, min_value=-32768, max_value=32767)
                elif isinstance(field, fields.IntegerField):
                    set_integer(instance, field)
                elif isinstance(field, fields.FloatField):
                    set_float(instance, field)
                elif isinstance(field, fields.CharField):
                    set_chars(instance, field)
                elif isinstance(field, (CKEditorField, CKEditorUploadField)):
                    set_text(instance, field, paragraphs=random.randint(3, 10), html=True)
                elif isinstance(field, fields.TextField):
                    set_text(instance, field, paragraphs=random.randint(1, 3))
                elif isinstance(field, fields.DateField):
                    set_date(instance, field)
                elif isinstance(field, fields.DecimalField):
                    set_decimal(instance, field, max_digits=6)
                elif isinstance(field, fields.URLField):
                    set_url(instance, field)
                elif isinstance(field, StdImageField):
                    set_stdimage(instance, field)
                elif isinstance(field, ImageField):
                    set_image(instance, field, width=1920, height=1440)
                elif isinstance(field, FileField):
                    set_image(instance, field, width=800, height=600)
                else:
                    print('WARNING: unknown type of field "%s": %s' % (field.name, type(field)))
                    continue

            instance.full_clean()
            instance.save()

            for field, model in Model._meta.get_m2m_with_model():
                set_m2m(instance, field)

        print('Done')
