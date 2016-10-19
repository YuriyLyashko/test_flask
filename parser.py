import json, csv, xlrd, os


def get_extension(incoming_file):
    '''
    Get extension from incoming file
    :param file: incoming file
    :return: file extension
    >>> get_extension('eFw3Cefj.json')
    'json'
    >>> get_extension('qwerty.doc')
    'doc'
    '''
    return os.path.splitext(incoming_file)[1][1:]


def read_json(incoming_file):
    '''
    Read from incoming JSON file
    :param file: incoming file
    :return: information from incoming file in dict format
    >>> read_json('eFw3Cefj.json') #doctest: +ELLIPSIS
    {...}
    '''
    with open(incoming_file) as json_data:
        return json.load(json_data)


def read_csv(incoming_file):
    '''
    Read from incoming CSV file
    :param file: incoming file
    :return: information from incoming file in dict format
    >>> read_csv('eFw3Cefj.csv') #doctest: +ELLIPSIS
    {...}
    '''
    with open(incoming_file) as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        structure = [key for key in data[0].keys()]
        return {'structure': structure, 'data': data}


def read_xls(incoming_file):
    '''
    Read from incoming XLS file
    :param file: incoming file
    :return: information from incoming file in dict format
    >>> read_xls('eFw3Cefj.xls') #doctest: +ELLIPSIS
    {...}
    '''
    data = []
    rb = xlrd.open_workbook(incoming_file, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if rownum == 0:
            structure = row
        else:
            d = {}
            for key, value in zip(structure, row):
                d[key] = value
            data.append(d)
    return {'structure': structure, 'data': data}


support_extensions = {
    'json': read_json,
    'csv': read_csv,
    'xls': read_xls
}


def read(incoming_file):
    '''
    Reading data from incoming file
    :param file: incoming file
    :return: table with data from incoming file
    >>> read('eFw3Cefj.json') #doctest: +ELLIPSIS
    {...}
    >>> read('eFw3Cefj.csv') #doctest: +ELLIPSIS
    {...}
    >>> read('eFw3Cefj.xls') #doctest: +ELLIPSIS
    {...}
    '''
    file_extension = get_extension(incoming_file)
    if file_extension not in support_extensions:
        raise ValueError('not supported file_extension')
    return support_extensions[file_extension](incoming_file)




if __name__ == '__main__':
    import doctest
    doctest.testmod()




