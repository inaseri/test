from jdatetime import datetime as jdatetime
from datetime import datetime,time
from django import template
from dateutil import tz
import pytz
register = template.Library()

@register.filter("jdate")
def jdate(value,format):
    print(type(value))
    if type(value)==type(""):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    try:
        value = value.replace(tzinfo=tz.gettz('UTC')).astimezone(pytz.timezone('Asia/Tehran'))
    except:
        pass
    try:
        return jdatetime.fromgregorian(datetime=value).strftime(format)
    except:
        return jdatetime.fromgregorian(date=value).strftime(format)

@register.filter("sectotime")
def sectotime(value):
    sec = str(value % 60)
    min = str(value//60%60)
    if len(sec) <2:
        sec = "0"+sec
    if len(min)<2:
        min = "0"+min

    return str(value // 3600)+":"+min+":"+sec

@register.filter
def at_index(array, index):
    return array[index]

@register.filter("convertToStr")
def convertToOut(value,index):
    preWord = str(value)
    number = str(index)
    name = preWord + number
    return str(name)
