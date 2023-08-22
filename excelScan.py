import pandas as pd
from config import *
from typing import Final
from elapsed import *

config = loadConfig()

COL_PATH_IDX:Final = 7
COL_FILE_IDX:Final = 8

def pathStrip(path):
    return path.lstrip('/').lstrip('\\').rstrip('/').rstrip('\\')

@elapsed
def loadExcel():
    path = config['ENV']['EXCEL_FILE_PATH']
    data = pd.read_excel(path)

    deployList = []
    for idx, row in data.iterrows():
        if idx > 4 and len(row[COL_PATH_IDX]) > 0 :
            deployFile = {'path':pathStrip(row[COL_PATH_IDX]), 'file':row[COL_FILE_IDX]}
            deployList.append(deployFile)
    return deployList

if __name__ == '__main__':
    deployList = loadExcel()
    for s in deployList:
        print(s)