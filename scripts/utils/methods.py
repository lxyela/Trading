from datetime import datetime
import os

# check if the date arguments are in the correct format
def check_date_format(date, date_format='%Y-%m-%d'):
    try:
        d = datetime.strptime(date, date_format)
        return d
    except ValueError:
        raise ValueError('Incorrect date format for {}, should be {}'.format(date, date_format))

# check if the file exists
def check_file_folder(file):
    if not os.path.exists(file):
        raise ValueError('File or folder {} does not exist'.format(file))
    return file