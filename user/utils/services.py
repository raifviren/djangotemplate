"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
import os
from calendar import timegm
from collections import OrderedDict
from datetime import datetime, timedelta
import urllib.request, urllib.parse
from random import choice
from string import ascii_uppercase, digits
from urllib.request import urlopen
import ssl

from django.utils import timezone
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from rest_framework_jwt.settings import api_settings
from django.utils.text import slugify


def update_selected(instance, data, fields):
    for key in fields:
        setattr(instance, key, data.get(key, getattr(instance, key)))


def upload_image_to(instance, filename):
    """
    @summary: upload_image_to method helps models to upload images to S3
    @param instance: models.Model object
    @param filename: string
    @return: string
    """
    CODE_TYPE = os.environ.get('CODE_TYPE', 'LOCAL')
    filename, filename_ext = os.path.splitext(filename)
    if filename_ext in ['.jpg', '.png', '.jpeg', '.gif']:
        category = 'image'
    elif filename_ext in ['.pdf', '.doc', '.docx', '.csv', '.ppt', '.pptx', '.txt']:
        category = 'doc'
    elif filename_ext in ['.avi', '.mp4', '.mov', '.mpeg', '.flv', '.wmv', '.3gp', '.mkv']:
        category = 'video'
    else:
        category = 'other'
    object_type = instance.__class__.__name__
    return '%s/%s/%s/%s%s%s' % (
        CODE_TYPE,
        object_type.lower(),
        category,
        filename[:30], timezone.now().strftime("%Y%m%d%H%M%S%s"),
        filename_ext.lower(),
    )


def get_file_from_url(image_url):
    """
    @summary: download file from given url
    @param image_url: string
    @return: File instance
    """

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    filename = urllib.parse.urlparse(image_url).path.split('/')[-1]
    req = urllib.request.Request(image_url, )
    response = urlopen(req, context=ctx)
    data = response.read()  # Get Response
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(data)
    img_temp.flush()
    return File(img_temp, name=filename)


def jwt_payload_handler_custom(user):
    username = user.username

    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if user.email:
        payload['email'] = user.email
    # if isinstance(self.pk, uuid.UUID):
    payload['user_id'] = str(user.pk)

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    return payload


def week_range(today_date):
    """Find the first/last day of the week for the given day.
    Assuming weeks start on Sunday and end on Saturday.
    Returns a tuple of ``(start_date, end_date)``.
    """

    # today_date = date.today()
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = today_date.isocalendar()
    # Find the first day of the week.
    if dow == 7:
        # Since we want to start with Sunday, let's test for that condition.
        start_date = today_date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = today_date - timedelta(dow)
    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + timedelta(6)
    return start_date, end_date


def random_code(n):
    chars = ascii_uppercase + digits
    return ''.join(choice(chars) for i in range(n))


def strip_string(string):
    stopwords = ['is', 'a', 'at', 'is', 'he', 'she', 'his', 'him', 'her', 'the', 'are', 'were', 'an', 'to',
                 'for', 'of', 'and', 'or']
    querywords = string.split('-')

    resultwords = [word.lower() for word in querywords if word.lower() not in stopwords]
    result = '-'.join(list(OrderedDict.fromkeys(resultwords)))
    return result[:94]


def get_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = strip_string(slug)
    ModelClass = model_instance.__class__

    while ModelClass._default_manager.filter(
            **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = '{}-{}'.format(slug, random_code(6))
    return unique_slug


def s3_upload_file(data, output_filename):
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    k = Key(bucket)
    k.key = 'temp-downloads/{}'.format(uuid.uuid4().hex)
    k.set_contents_from_file(data)

    download_url = k.generate_url(
        expires_in=60,
        response_headers={
            'response-content-type': 'text/csv',
            'response-content-disposition': 'attachment; filename={}'.format(
                output_filename),
        }
    )
    return download_url

def update_selected(instance, data, fields):
    for key in fields:
        setattr(instance, key, data.get(key, getattr(instance, key)))
