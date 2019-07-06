import pandas as pd


def completeMissingVals(df, numeric_cols):
    """
    Receive a df (pd.DataFrame) and a list of columns in the df.
    The function will fill all na cells.
    if the column name is in numeric_cols it will replace in with the average number of that column
    otherwise it will replace it with the most common value in that column.
    :param df: pd.DataFrame
    :param numeric_cols: list containing numeric columns in df wanting to fillna by mean value
    :return:
    """
    df.fillna(df.mean()[numeric_cols], inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)


def discrete_numeric(df, numeric_cols, bins):
    """
    Receive a df (pd.DataFrame), a list of columns in the df and number of bins for discretion
    Preform discretion to all columns in numeric_cols to #bins
    :param df: pd.DataFrame
    :param numeric_cols: list containing numeric columns to perform discretion on
    :param bins: int, the number of bins
    :return:
    """
    for col in numeric_cols:
        labels = list(range(1, bins + 1))
        df[col] = pd.cut(df[col], bins=bins, labels=labels)


def get_numeric_categorical_lists(text):
    """
    Receive list of str's containing the structure of the data.
    analyze the text and return a dict of category to possible attributes
    and a list of the numeric attributes
    :param text: list of str
    :return: (dict: categorical to possible attributes, list: numeric attributes)
    """
    numeric = []
    categorical = {}

    for line in text:
        attribute = line.split()[1]
        if line.find('{') >= 0:
            cat = line[line.find('{') + 1: line.find('}')]
            categorical[attribute] = cat.split(',')
        else:
            numeric.append(attribute)
    return categorical, numeric


def createStructureDic(categorical, numerical, bins ):
    """
    Transform the categorical dict and numerical list attributes to a dict
    :param categorical: dict - from columns name to possible attributes
    :param numerical: list
    :param bins: int, number of bins to assign to the numerical attributes
    :return:
    """
    struct_dic = {}
    struct_dic.update(categorical)

    for num_col in numerical:
        struct_dic[num_col] = list(map(str,range(1, bins + 1)))

    return struct_dic


