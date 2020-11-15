from openpyxl import load_workbook
import pandas as pd
from necInfo import NecInfo


class NecPollbook(NecInfo):
    def __init__(self):
        super().__init__()
        self._book_type = ''

    def open(self, in_file, out_file):
        ws = load_workbook(in_file)['Sheet1']
        self._get_sg_info(ws)
        self._get_labels(ws)
        self._read_df(in_file)
        print(self.items.head(20))
        self.items.to_excel(out_file)

    def _get_sg_info(self, sheet):
        if sheet[2][0].value == '선거인수현황':
            self._get_sg_info_legacy(sheet)
            self._book_type = 'legacy'
        else:
            self._get_sg_info_last(sheet)
            self._book_type = 'last'

    def _get_sg_info_last(self, sheet):
        self._sg_info['대수'] = int(sheet[2][0].value[2:4])
        self._sg_info['선거명'] = sheet[2][0].value.replace(']', '').split(' ')[1]
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['시도'] = texts[0]
        self._sg_info['구시군'] = texts[1]

    def _get_sg_info_legacy(self, sheet):
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['대수'] = int(texts[0][1:3])
        self._sg_info['선거명'] = texts[1]
        self._sg_info['시도'] = texts[2]
        self._sg_info['구시군'] = texts[3]

    def _get_labels(self, ws):
        labels = self._read_rows(ws, 4)

        for index, label in enumerate(labels):
            if str(type(label)) == "<class 'str'>":
                labels[index] = label.replace('\n', ' ')
        labels[4] = labels[3]
        labels[3] = '남여'
        print(labels)
        self.labels = labels

    def _read_df(self, in_file):
        df = pd.read_excel(in_file, skiprows=4)
        df.columns = self.labels
        df = df[df.columns[df.columns.notna()]]
        if self._book_type == 'legacy':
            df.rename({'인구수 (선거인명부작성 기준일 현재)': '인구수 (선거인명부작성 기준일현재)',
                       '확정 선거인수': '확정된 국내선거인수 (A)',
                       '인구대비 선거인 비율(%)': '인구수에 대한 국내선거인수 비율(%)',
                       '거소투표(부재자) 신고인명부 등재자수': '거소투표 신고인명부 등재자수'},
                      axis='columns', inplace=True)
            df.insert(6, '선상투표 신고인명부 등재자수', 0)
            df.insert(7, '재외 선거인수 (B)', 0)
        else:
            df.drop('총선거인수 (A + B)', axis=1, inplace=True)

        df['읍면동명'] = self._fill_column_with_previous_cell(df, df.columns.get_loc('읍면동명'))
        df['투표구명'] = self._fill_column_with_this_text(df, df.columns.get_loc('투표구명'), '전체')
        df['성별'] = df['남여']
        df.drop('남여', axis=1, inplace=True)
        df.drop('인구수에 대한 국내선거인수 비율(%)', axis=1, inplace=True)

        endIndex = len(df.columns) - 1
        for col_name in df.columns[2:endIndex]:
            df[col_name] = df.apply(lambda x: int(x[col_name].split('\n')[0].replace(',', ''))
                                    if str(type(x[col_name])) == "<class 'str'>"
                                    else x[col_name],
                                    axis=1)

        df['미성년자수'] = df['인구수 (선거인명부작성 기준일현재)'] - df['확정된 국내선거인수 (A)']
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

        df['인구대비 국내선거인 비율'] = df['확정된 국내선거인수 (A)'] / df['인구수 (선거인명부작성 기준일현재)'] * 100
        df['인구대비 미성년자 비율'] = 100 - df['인구대비 국내선거인 비율']
        df['국내선거인 중 남성비율'] = df['국내선거인 중 남성수'] / df['확정된 국내선거인수 (A)'] * 100
        df['국내선거인 중 여성비율'] = df['국내선거인 중 여성수'] / df['확정된 국내선거인수 (A)'] * 100
        df['세대당 인구수'] = df['인구수 (선거인명부작성 기준일현재)'] / df['세대수']
        df['세대당 국내선거인수'] = df['확정된 국내선거인수 (A)'] / df['세대수']
        df['세대당 미성년자수'] = df['미성년자수'] / df['세대수']
        df['세대당 남성수'] = df['국내선거인 중 남성수'] / df['세대수']
        df['세대당 여성수'] = df['국내선거인 중 여성수'] / df['세대수']

        df.insert(0, '읍면동투표구명', df['읍면동명'] + df['투표구명'])
        df.insert(1, '대수', self._sg_info['대수'])
        df.insert(2, '선거명', self._sg_info['선거명'])
        df.reset_index(inplace=True, drop=True)
        self.items = df

    def func(self):
        pass
