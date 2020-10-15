from openpyxl import load_workbook
import pandas as pd
from necInfo import NecInfo


class NecPollbook(NecInfo):
    def __init__(self):
        super().__init__()

    def open(self, filename):
        ws = load_workbook(filename)['Sheet1']
        self._get_sg_info(ws)
        self._get_labels(ws)
        self._read_df(filename)
        print(self.sg_pollbook.head(20))

    def _get_sg_info(self, sheet):
        self._sg_info['대수'] = int(sheet[2][0].value[2:4])
        self._sg_info['선거명'] = sheet[2][0].value.replace(']', '').split(' ')[1]
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['시도'] = texts[0]
        self._sg_info['선거구(구시군)'] = texts[1]

    def _get_labels(self, ws):
        labels = self._read_rows(ws, 4)

        for index, label in enumerate(labels):
            if str(type(label)) == "<class 'str'>":
                labels[index] = label.replace('\n', ' ')
        labels[4] = labels[3]
        labels[3] = '성별'
        print(labels)
        self.labels = labels

    def _read_df(self, filename):
        df = pd.read_excel(filename, skiprows=3)
        df.columns = self.labels

        df[df.columns[0]] = self._get_filled_column(df, 0)
        df[df.columns[1]] = self._get_filled_column(df, 1)
        df[df.columns[2]] = self._get_filled_column(df, 2)
        df[df.columns[10]] = self._get_filled_column(df, 10)
        df[df.columns[11]] = self._get_filled_column(df, 11)
        df = df[df.columns[df.columns.notna()]]

        df.drop(df.index[df['읍면동명'] == '합계'], axis=0, inplace=True)
        df.drop(df.index[df['투표구명'] == '소계'], axis=0, inplace=True)
        df.drop(df.index[df['성별'] == '계'], axis=0, inplace=True)

        for col_name in df.columns[4:9]:
            df[col_name] = df.apply(lambda x: int(x[col_name].split('\n')[0].replace(',', ''))
                                    if str(type(x[col_name])) == "<class 'str'>"
                                    else x[col_name],
                                    axis=1)
        for col_name in df.columns[2:3]:
            df[col_name] = df.apply(lambda x: int(x[col_name].split('\n')[0].replace(',', ''))
                                    if str(type(x[col_name])) == "<class 'str'>"
                                    else x[col_name],
                                    axis=1)
        for col_name in df.columns[10:11]:
            df[col_name] = df.apply(lambda x: int(x[col_name].split('\n')[0].replace(',', ''))
                                    if str(type(x[col_name])) == "<class 'str'>"
                                    else x[col_name],
                                    axis=1)

        self.sg_pollbook = df
        df.to_excel('result.xlsx')
