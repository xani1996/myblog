from . import jalali
from django.utils import timezone


def jalali_converter(time):
    time = timezone.localtime(time)
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_str_out = jalali.Gregorian(time_to_str).persian_tuple()
    output = f"{time_to_str_out[0]}/{time_to_str_out[1]}/{time_to_str_out[2]}"
    return output
