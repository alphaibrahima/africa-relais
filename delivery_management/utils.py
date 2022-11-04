import os
import base64
import random
import string

from django.core.files.base import ContentFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import EmailValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9347326742427)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


def email_validation(value):
    validator = EmailValidator()
    validator(value)
    return value


def generate_key():
    key = "".join(random.choices(string.digits, k=6)).upper()
    return key


def get_paginator(qs, page_size, page, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


def save_base_64(file):
    format, imgstr = file.split(";base64,")
    ext = format.split("/")[-1]
    data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
    return data


def format_date(date_object):
    day_of_month = date_object.strftime("%d")
    month = date_object.strftime("%m")
    year = date_object.strftime("%Y")
    return "{}-{}-{}".format(day_of_month, month, year)


def trail_string(str):
    if str:
        return str.strip()
    else:
        return ""


def round_to_five(value, base=5):
    return base * round(value / base)
    # return int(value) - int(value) % int(base)


def get_price(result):
    if result == 2:
        price = 800
    elif result == 3:
        price = 1000
    elif result == 4:
        price = 900
    else:
        price = 700
    return price


def calculate_price(zone_a, zone_b):
    print(zone_a == zone_b)
    price = 0
    if zone_a > zone_b:
        result = (zone_a - zone_b) + 1
        price = get_price(result)
    elif zone_a < zone_b:
        result = (zone_b - zone_a) + 1
        price = get_price(result)
    elif zone_a == zone_b:
        price = 700
    return price


def decode_utf8(line_iterator):
    for line in line_iterator:
        yield line.decode("utf-8")
