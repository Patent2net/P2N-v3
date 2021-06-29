import re
import pandas as pd

csv_directory = 'CSVSets'
csv_separator = ';'

def read_from_request_field(request_field):
    fic = '../' + csv_directory + '/' + get_csv_file_name_from_request_field(request_field)

    print(fic)
    with open(fic, 'r'):
        return pd.read_csv(fic, sep =csv_separator)

def csv_file_name_to_request_field(csv_file): 
    return 'CSV(' + csv_file + ')'

def get_csv_file_name_from_request_field(requet_field):
    csv_search = re.search('CSV\((.*)\)', requet_field, re.IGNORECASE)

    if csv_search:
        return csv_search.group(1)
    else:
        return None