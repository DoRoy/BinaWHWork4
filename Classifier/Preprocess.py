import pandas as pd


def completeMissingVals(df, numeric_cols):
    df.fillna(df.mean()[numeric_cols], inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)


def discrete_numeric(df, numeric_cols, bins):
    max_vals = df.max()
    min_vals = df.min()
    for col in numeric_cols:
        # bin_size = (max_vals[col] - min_vals[col])/bins
        # bins_list = np.arange(min_vals[col], max_vals[col]+0.02, bin_size)
        labels = list(range(1, bins + 1))
        df[col] = pd.cut(df[col], bins=bins, labels=labels)


def get_numeric_categorical_lists(text):
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
    struct_dic = {}
    struct_dic.update(categorical)

    for num_col in numerical:
        struct_dic[num_col] = list(map(str,range(1, bins + 1)))

    return struct_dic


