import pandas as pd
import openpyxl
import pprint as pprint

def writeToExcel(object,file):
    df = pd.DataFrame(list(object))
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]

    writer = pd.ExcelWriter(file, engine='openpyxl')

    wb = openpyxl.load_workbook(file)
    rows_count = wb.worksheets[0].max_row
    writer.book = wb
    writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)

    if rows_count > 1:
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer,encoding='utf-8',header=None, startrow=rows_count)

    else:
        df.to_excel(writer, encoding='utf-8')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
