import os
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

def get_csv_directory():
    return csv_directory


def get_headers(csv_file_name):
    os.chdir("/home/p2n/P2N-V3/Patent2Net")
    fic = '../' + csv_directory + '/' + csv_file_name

    with open(fic, 'r'):
        df = pd.read_csv(fic, sep =csv_separator, index_col=0, nrows=0)

        return df.columns.tolist()