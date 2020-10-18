import openpyxl
import pandas as pd
from abc import *


class NecInfo(metaclass=ABCMeta):
    def __init__(self):
        self._sg_info = {'선거명': '',
                         '대수': '',
                         '시도': '',
                         '선거구(시도)': '',
                         '선거구(구시군)': ''}
        pass

    def _read_rows(self, sheet, row_index):
        labels = []
        for column in sheet[row_index]:
            value = column.value
            labels.append(value)
        return labels

    def _get_filled_column(self, df, col_index):
        col = []
        previous = ''
        for index, row in df.iterrows():
            value = row[df.columns[col_index]]
            if str(type(value)) == "<class 'str'>":
                value = value.strip()
                if value == '':
                    value = previous
            else:
                value = previous
            col.append(value)
            previous = value
        return col

    def _get_text_filled_column(self, df, col_index, text):
        col = []
        previous = text
        for index, row in df.iterrows():
            value = row[df.columns[col_index]]
            if str(type(value)) == "<class 'str'>":
                value = value.strip()
                if value == '':
                    value = previous
            else:
                value = previous
            col.append(value)
        return col
