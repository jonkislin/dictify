# command line tool

import documenter

# this section will only run if we run the script from the command line
if __name__ == '__main__':

    filenames = argv[1:]  # python is 0-indexed. index 0 is the name of the script
    # this takes us from index 0 to the end of the list of arguments we passed
    # when running the script with `python dictify.py x y z`

    # User Instructions
    print('''
    Data files to be dictify\'d (documented) are passed
    as arguments in the command line
    e.g. "python dictify.py data1.csv data2.xlsx data3.csv data4.xls"

    Make sure the datafile(s) you want to dictify
    is/are the in the same folder as this 'dictify' script,
    or else specify the absolute path when running the script.

    This script will not run if you do not have write-privileges to the
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

    output_choice = ""
    while output_choice is not 'excel' or output_choice is not 'csv':
        print('Write output file as flat csv or excel file with sheets?')
        output_choice = input('Type "csv" for csv and "excel" for excel')

    if output_choice is 'excel':
        writer_excel = pd.ExcelWriter(dict_name + '.xlsx')
    elif output_choice is 'csv':
        writer_csv = pd.DataFrame()
    else:
        print('Error occured with output format choice')
        sleep(2)
        quit()

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
                print('Only the first sheet will be dictify\'d''')
                sleep(2)
            else:
                print('Invalid file extension. Please rerun program')
                quit()
        except:
            print('Unknown error occured. Please check files and rerun')
            quit()

        print(f'Dictifying {filename}...')

        # Write to file, one input file at a time
        dd = documenter(data)  # calling our function from earlier

        if output_choice is 'excel':
            dd.to_excel(writer, sheet_name=sheetname, index=False)
        elif output_choice is 'csv':

    if output_choice is 'excel':
        writer.save()  # saves and closes the dictionary excel file

    print('Dictifying complete!')
    print(f'Find your file as {dict_name}.xlsx')
    sleep(1)
