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
        print(self.items.head(20))

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
        df = df[df.columns[df.columns.notna()]]

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
        df.insert(0, '읍면동투표구명', df['읍면동명'] + df['투표구명'])
        # df.set_index(['읍면동명', '투표구명'], inplace=True)

        df['국내선거인 중 남성수'] = ''
        df['국내선거인 중 여성수'] = ''
        sung = df.columns.get_loc('성별')
        man = df.columns.get_loc('국내선거인 중 남성수')
        woman = df.columns.get_loc('국내선거인 중 여성수')
        number = df.columns.get_loc('확정된 국내선거인수 (A)')

        for index in range(df.index.size):
            if df.iloc[index, sung] == '계':
                df.iloc[index, man] = df.iloc[index+1, number]
                df.iloc[index, woman] = df.iloc[index+2, number]

        df = df[df['성별'] == '계']
        df.drop('성별', axis=1, inplace=True)
        df['국내선거인 중 남성비율'] = df['국내선거인 중 남성수'] / df['확정된 국내선거인수 (A)'] * 100
        df['국내선거인 중 여성비율'] = df['국내선거인 중 여성수'] / df['확정된 국내선거인수 (A)'] * 100
        df['인구수에 대한 국내선거인수 비율(%)'] = df['확정된 국내선거인수 (A)'] / df['인구수 (선거인명부작성 기준일현재)'] * 100
        df['세대당 국내선거인수'] = df['확정된 국내선거인수 (A)'] / df['세대수']
        df['세대당 자녀수'] = (df['인구수 (선거인명부작성 기준일현재)'] - df['확정된 국내선거인수 (A)']) / df['세대수']

        self.items = df
        df.to_excel('nec_pollbook.xlsx')

    def func(self):
        pass