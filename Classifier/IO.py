import pandas as pd

def readCSV(path):
    """
    Read the CSV file in the given path
    :param path: The path of the CSV file wanting to open
    :return: pd.DataFrame
    """
    df = pd.read_csv(path)
    return df


def readTXT(path):
    """
    Read the file in the given path for read only
    :param path: The path of the file wanting to open
    :return: list containing each line as an item.
    """
    with open(path,'r') as file:
        file_lines = file.readlines()
    return file_lines


def writeResults(path, text):
    """
    Write a text to a file in the path. the content is deleted if exist
    :param path: the path to the file wanting to create of write in.
    :param text: the text wanting to write as str
    :return:
    """
    with open(path, 'w+') as file:
        file.write(text)
