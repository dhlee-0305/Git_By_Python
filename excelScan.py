import pandas as pd
from config import *

config = loadConfig()

def pathStrip(path):
    return path.lstrip('/').lstrip('\\').rstrip('/').rstrip('\\')

def loadExcel():
    path = config['ENV']['EXCEL_FILE_PATH']
    data = pd.read_excel(path)

    deployList = []
    for idx, row in data.iterrows():
        if idx > 4 and len(row[7]) > 0 :
            deployFile = [pathStrip(row[7]), row[8]]
            deployList.append(deployFile)
    return deployList

