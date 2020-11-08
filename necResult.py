from openpyxl import load_workbook
import pandas as pd
from necInfo import NecInfo


class NecResult(NecInfo):
    def __init__(self, necId):
        super().__init__()
        self.id = necId
        pass

    def open(self, in_file, out_file):
        ws = load_workbook(in_file)['Sheet1']
        self._get_sg_info(ws)
        self._get_labels(ws)
        self._read_df(in_file)
        print(self.items.head(30))
        self.items.to_excel(out_file)

    def _get_sg_info(self, sheet):
        if self.id == 'assembly21':
            self._get_sg_info1(sheet)
        elif self.id == 'assembly20':
            self._get_sg_info2(sheet)
        elif self.id == 'president19':
            self._get_sg_info3(sheet)

    def _get_sg_info1(self, sheet):
        self._sg_info['대수'] = int(sheet[2][0].value[2:4])
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['선거명'] = texts[0]
        self._sg_info['시도'] = texts[1]
        self._sg_info['선거구'] = texts[2]
        self._sg_info['구시군'] = texts[3]
        print(self._sg_info)

    def _get_sg_info2(self, sheet):
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['대수'] = int(texts[0][1:3])
        self._sg_info['선거명'] = texts[2]
        self._sg_info['시도'] = texts[3]
        self._sg_info['구시군'] = texts[4]
        print(self._sg_info)

    def _get_sg_info3(self, sheet):
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['대수'] = int(texts[0][1:3])
        self._sg_info['선거명'] = texts[1]
        self._sg_info['시도'] = texts[2]
        self._sg_info['구시군'] = texts[3]
        self._sg_info['선거구'] = '-'
        print(self._sg_info)

    def _get_labels(self, ws):
        labels = self._read_rows(ws, 4)
        sub_labels = self._read_rows(ws, 5)

        for index, sub_label in enumerate(sub_labels):
            type(sub_label)
            if str(type(sub_label)) == "<class 'str'>":
                sub_label = sub_label.replace(' ', '')
                if sub_label != '':
                    labels[index] = sub_label

        for index, label in enumerate(labels):
            if str(type(label)) == "<class 'str'>":
                labels[index] = label.replace('\n', ' ')
        print(labels)
        self.labels = labels

    def _read_df(self, filename):
        df = pd.read_excel(filename, skiprows=5, header=None)
        df.columns = self.labels

        if '선거구명' not in self.labels:
            df.insert(0, '선거구명', self._sg_info['선거구'])

        if '읍면동명' not in self.labels:
            df.insert(1, '읍면동명', df['투표구명'])
            df['투표구명'] = df['투표구명'].apply(lambda x: ''
                                          if x in ['계', '거소·선상투표', '관외사전투표', '국외부재자투표', '잘못 투입·구분된 투표지']
                                          else x)
            col = []
            for index, value in enumerate(df['읍면동명']):
                if value == '소계':
                    value = df['읍면동명'][index + 2]
                elif value == '관내사전투표':
                    value = df['읍면동명'][index + 1]
                if '동제' in value:
                    texts = value.split('동제')
                    value = texts[0] + '동'
                col.append(value)
                print(index, value)

        df['선거구명'] = self._get_filled_column(df, 0)
        df['읍면동명'] = self._get_filled_column(df, 1)
        df['투표구명'] = self._get_text_filled_column(df, 2, '전체')

        df.drop('계', axis=1, inplace=True)
        df.drop(df.index[df['읍면동명'] == '계'], axis=0, inplace=True)
        df.drop(df.index[df['읍면동명'] == '합계'], axis=0, inplace=True)
        df = df[df.columns[df.columns.notna()]]
        for col_name in df.columns[3:]:
            df[col_name] = df.apply(lambda x: int(x[col_name].replace(',', ''))
                                    if str(type(x[col_name])) == "<class 'str'>"
                                    else x[col_name],
                                    axis=1)

        df.insert(0, '읍면동투표구명', df['읍면동명'] + df['투표구명'])
        df.insert(1, '대수', self._sg_info['대수'])
        df.insert(2, '선거명', self._sg_info['선거명'])
        # df.rename(columns={"선거인수": "선거일 선거인수"}, inplace=True)
        # df.set_index(['읍면동명', '투표구명'], inplace=True)
        df.reset_index(inplace=True, drop=True)
        self.items = df

    # nec_analysis.drop(nec_analysis.index[pd.isna(nec_analysis['투표구명'])], axis=0, inplace=True)
