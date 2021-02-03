from datetime import datetime
from time import time
# 'December 11, 2020'
def date_to_str(date):
    # 2012-05-01
    # yyyy-MM-dd
    splitted = date.split()
    # datetime_object = datetime.datetime.strptime(long_month_name, "%B")
    return '-'.join([splitted[2], str(datetime.strptime(splitted[0], "%B").month), splitted[1].replace(',', '')])