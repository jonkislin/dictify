from sys import argv  # so command line arguments can be accessed
from time import sleep  # pauses in the program to ease reading
import pandas as pd  # pandas for dataframe management and read/writing excel
import re  # regular expressions for string pattern matching


def calc_and_stitch(df):
    '''
    Function that creates a data-dictionary dataframe from a cleaned dataframe.
    ------
    args:
    df = Pandas dataframe.
    '''

    if 'filename' in locals():
        data_set = filename
    else:
        data_set = 'df'

    # misisng value counts
    na_perc = (df.isnull().sum() / len(df)) * 100

    # unique values in column
    count_distinct = df.nunique(dropna=False)

    # zip our components together
    zipper = list(zip(df.columns,
                      df.dtypes.replace({'object': 'text',
                                         'int64': 'integer',
                                         'float64': 'float',
                                         'bool': 'boolean'}),
                      na_perc,
                      count_distinct))

    names = ['Field Name', 'Data Type', 'Percent Missing Data', 'Distinct Value Count']

    # Tidying up and supplying blank fields
    data_dictionary = pd.DataFrame(zipper, columns=names)
    data_dictionary['Data Set'] = data_set
    data_dictionary['Description'] = ''  # to be manually entered later
    data_dictionary['Source for description'] = ''  # ditto

    # Reordering everything
    data_dictionary = data_dictionary[['Field Name',
                                       'Description',
                                       'Source for description',
                                       'Data Type',
                                       'Distinct Value Count',
                                       'Percent Missing Data',
                                       'Data Set']]

    return data_dictionary


# this section will only run if we run the script from the command line
if __name__ == '__main__':

    filenames = argv[1:]  # python is 0-indexed. index 0 is the name of the script
    # this takes us from index 0 to the end of the list of arguments we passed
    # when running the script with `python dictify.py x y z`

    # User Instructions
    print('''
    Files to be dictify\'d are passed
    as arguments in the command line
    e.g. "python dictify.py data1.csv data2.xlsx data3.csv data4.xls"

    Make sure the datafile(s) you want to dictify
    is/are the in the same folder as this script,
    or else specify the absolute path.

    Please note: this script will create one excel file with a
    data-dictionary sheet for every filename you passed to the command line.

    It will not run if you do not have write-privileges to the
    directory from which you ran it. Only excel and .csv files are supported.
    ''')

    if len(argv) < 2:
        print('ERROR: Please supply filename arguments and rerun script.')
        quit()
    else:
        pass

    print('Files to be dictify\'d:')
    for name in filenames:
        print(name)
    print('')

    # Output preparation
    dict_name = input('Please type a name for your data_dictionary > ')
    writer = pd.ExcelWriter(dict_name + '.xlsx')

    # Meat of the script

    for filename in filenames:

        filetype = re.findall(r'(\..*)', filename)[0]
        sheetname = re.findall(r'(.*)\..*', filename)[0]

        # Control Flow
        try:
            if filetype == '.csv':
                data = pd.read_csv(filename)
            elif filetype == '.xlsx' or filetype == '.xls':
                data = pd.read_excel(filename)
                print('NOTE: Excel spreadsheet detected.')
                print('Only first sheet will be dictify\'d''')
                sleep(2)
            else:
                print('Invalid file extension. Please rerun program')
                quit()
        except:
            print('Unknown error occured. Please check files and rerun')
            quit()

        print(f'Dictifying {filename}...')

        # Write to file, one input file at a time
        dd = calc_and_stitch(data)  # calling our function from earlier
        dd.to_excel(writer, sheet_name=sheetname, index=False)

    writer.save()  # saves and closes the dictionary excel file

    print('Dictifying complete!')
    print(f'Find your file as {dict_name}.xlsx')
    sleep(1)
