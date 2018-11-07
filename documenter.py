# Documenter
def documenter(df):  # to do -> add custom arguments
    '''
    Function that creates a data-dictionary dataframe from a cleaned dataframe.
    Returns a dataframe with the following columns:
    'Field Name' - the column name of each variable in the input frame
    'Description' - must be manually entered by user; will be empty
    'Source for description' - must be manually entered by user; will be empty
    'Data Type'
    'Distinct Value Count' - more meaningful for categorical fields
    'Percent Missing Data' - how many rows are NaNs/nulls/undefined for this field
    'Data Set' - name of the data file imported by the dictify script if
    run via the command line, or by the user if this function is imported
    a la carte.
    -------------
    args:
    df = Pandas dataframe.
    '''

    if 'filename' in locals():
        data_set = filename
    else:
        data_set = input('Please enter the name of this dataframe. > ')

    # percentage of datapoints that are missing
    na_perc = (df.isnull().sum() / len(df)) * 100

    # number of unique values in column
    count_distinct = df.nunique(dropna=True)

    # zip our components together
    zipper = list(zip(df.columns,
                      df.dtypes.replace({'object': 'text',
                                         'int64': 'integer',
                                         'float64': 'float',
                                         'bool': 'boolean'}),
                      na_perc,
                      count_distinct))

    names = ['Field Name',
             'Data Type',
             'Percent Missing Data',
             'Distinct Value Count']

    # Initializing the dataframe and supplying the remaining fields
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
