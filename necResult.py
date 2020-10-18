from openpyxl import load_workbook
import pandas as pd
from necInfo import NecInfo


class NecResult(NecInfo):
    def __init__(self):
        super().__init__()
        pass

    def open(self, filename):
        ws = load_workbook(filename)['Sheet1']
        self._get_sg_info(ws)
        self._get_labels(ws)
        self._read_df(filename)
        print(self.items.head(30))

    def _get_sg_info(self, sheet):
        self._sg_info['대수'] = int(sheet[2][0].value[2:4])
        texts = sheet[3][0].value[1:-1].split('][')
        self._sg_info['선거명'] = texts[0]
        self._sg_info['시도'] = texts[1]
        self._sg_info['선거구(시도)'] = texts[2]
        self._sg_info['선거구(구시군)'] = texts[3]
        print(self._sg_info)

    def _get_labels(self, ws):
        labels = self._read_rows(ws, 4)
        sub_labels = self._read_rows(ws, 5)

        for index, sub_label in enumerate(sub_labels):
            if str(type(sub_label)) == "<class 'str'>":
                labels[index] = sub_label

        for index, label in enumerate(labels):
            if str(type(label)) == "<class 'str'>":
                labels[index] = label.replace('\n', ' ')
        print(labels)
        self.labels = labels

    def _read_df(self, filename):
        df = pd.read_excel(filename, skiprows=5)
        df.columns = self.labels

        df[df.columns[0]] = self._get_filled_column(df, 0)
        df[df.columns[1]] = self._get_text_filled_column(df, 1, '전체')

        # df.drop(df.index[df['투표구명'] == '소계'], axis=0, inplace=True)
        df.drop('계', axis=1, inplace=True)
        df = df[df.columns[df.columns.notna()]]
        for col_name in df.columns[2:]:
            df[col_name] = df.apply(lambda x: int(x[col_name].replace(',', ''))
                                    if str(type(x[col_name])) == "<class 'str'>"
                                    else x[col_name],
                                    axis=1)

        # df.rename(columns={"선거인수": "선거일 선거인수"}, inplace=True)
        # df.rename(columns={"투표수": "선거일 투표수"}, inplace=True)
        df.insert(0, '읍면동투표구명', df['읍면동명'] + df['투표구명'])
        # df.set_index(['읍면동명', '투표구명'], inplace=True)
        df.reset_index(inplace=True, drop=True)
        self.items = df
        df.to_excel('nec_result.xlsx')
    # nec_analysis.drop(nec_analysis.index[pd.isna(nec_analysis['투표구명'])], axis=0, inplace=True)
