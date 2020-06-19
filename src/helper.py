
from datetime import date, datetime, timedelta
from os.path import isdir
from os import mkdir
import pickle

def count_number_digits(num):
    if isinstance(num, float):
        num = str(num).split('.', 1)[0]
    elif isinstance(num, int):
        num = str(num)
    else:
        raise ValueError('Not int or float object')
    return len(list(num))

def check_datetime_instance(date_time):
    if not isinstance(date_time, datetime) or not isinstance(date_time, date):
        raise ValueError('Not datetime or date object')

def datetime_to_datetime_string(date_time, form):
    check_datetime_instance(date_time)
    return date_time.strftime(form)

def datetime_to_isoformat(date_time):
    check_datetime_instance(date_time)
    return date_time.isoformat()

def datetime_to_timestamp(date_time):
    check_datetime_instance(date_time)
    return date_time.timestamp()

def datetime_string_to_timestamp(date_time, form):
    if isinstance(date_time, str):
        date_time = datetime_string_to_datetime(date_time, form)
    return float(datetime_to_timestamp(date_time))

def datetime_string_to_datetime(string, form):
    if not isinstance(string, str):
        raise ValueError('Not string object')
    return datetime.strptime(string, form)

def timestamp_to_datetime(timestamp):
    count = count_number_digits(timestamp)
    if count < 10:
        raise ValueError('Timestamp consist of 10 digits')
    if count > 10:
        timestamp = timestamp/(10**(count-10))
    return datetime.fromtimestamp(timestamp)

def timestamp_to_datetime_string(timestamp, form):
    return datetime_to_datetime_string(timestamp_to_datetime(timestamp), form)

def datetime_change_format(source, input_format, output_format):
    if isinstance(source, datetime):
        return datetime_string_to_datetime(
            datetime_to_datetime_string(source, output_format),
            output_format
        )

def pickle_dump(file_path, obj):
    dest_folder = file_path.rsplit('/',1)[0]
    
    if not isdir(dest_folder): 
        mkdir(dest_folder) # Create folder if it does not exist

    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def pickle_load(file_path):
    dest_folder = file_path.rsplit('/',1)[0]

    if not isdir(dest_folder): 
        print(f'{dest_folder} not found')
        return

    with open(file_path, 'rb') as f:
        return pickle.load(f)

