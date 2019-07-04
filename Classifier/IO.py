import pandas as pd

def readCSV(path):
    df = pd.read_csv(path)
    return df


def readTXT(path):
    with open(path,'r') as file:
        file_lines = file.readlines()
    return file_lines


def writeResults(path, text):
    with open(path, 'w+') as file:
        file.write(text)
