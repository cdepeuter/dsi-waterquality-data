#coding=utf-8
import pyPdf
import pandas as pd
from pyPdf import PdfFileWriter, PdfFileReader
from tabula import read_pdf

file_Path = "/Users/haiki/Documents/2017fall/Capstone/46-17.pdf"
with open(file_Path, "rb") as input_file:
    input1 = PdfFileReader(input_file)
    numPages = input1.getNumPages()

df = read_pdf(file_Path, pages="1-"+str(numPages),  multiple_tables=True)
param_out = df[0][5].str.split(' ',expand=True)
level_out = df[0][6].str.split(' ',expand=True)
param_out = param_out.dropna()
level_out = level_out.dropna()
for i in range(1, len(df)):
    param_table = df[i][5].str.split(' ',expand=True)
    param_table = param_table.dropna()
    param_table = param_table.drop(param_table.index[0])
    param_out = pd.concat([param_out, param_table], axis=0)
    level_table = df[i][6].str.split(' ',expand=True)
    level_table = level_table.dropna()
    level_table = level_table.drop(level_table.index[0])
    level_out = pd.concat([level_out, level_table], axis=0)
level_out=level_out.reset_index(drop=True)
param_out=param_out.reset_index(drop=True)
level_out.to_csv("level.csv", sep=",", encoding='utf-8')
param_out.to_csv("param.csv", sep=",", encoding='utf-8')