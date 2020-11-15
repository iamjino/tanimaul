import pandas as pd


def day_voter(x):
    result = ''
    if x['사전투표수'] > 0:
        result = x['투표수']
    return result


class NecAnalysis():
    def __init__(self, nec_result, nec_pollbook):
        nec_result_part = nec_result.items[['읍면동투표구명', '읍면동명', '투표구명', '선거인수', '투표수', '기권수']].copy()
        nec_result_part.rename(columns={'읍면동명': '읍면동명_결과', '투표구명': '투표구명_결과'}, inplace=True)
        self.na = pd.merge(nec_pollbook.items, nec_result_part, on='읍면동투표구명', how='right')
        self.score = nec_result.items.copy()
        self.dongs = self.na['읍면동명'].dropna().unique()
        self.score_dong_unique = self.score['읍면동명'].unique()
        self.score_place_unique = self.score['투표구명'].unique()

    def get_place_pre_sum(self):
        self.na['당일투표수'] = ''
        self.na['사전투표수'] = self.na['확정된 국내선거인수 (A)'] - self.na['선거인수']

        self.na['당일투표수'] = self.na.apply(day_voter, axis=1)

        self.na.drop(self.na.index[self.na['투표구명'] == '소계'], axis=0, inplace=True)
        self.na.set_index(['읍면동명_결과', '투표구명_결과'], inplace=True)
        self.na['관내사전투표수'] = ''
        for dong in self.dongs:
            dong_pre_sum = self.na.loc[(dong, '관내사전투표'), '선거인수']
            dong_pre = self.na.loc[dong, '사전투표수'].sum()
            dong_pre_in_ratio = dong_pre_sum / dong_pre
            for place in self.na.loc[dong].index:
                self.na.loc[(dong, place), '관내사전투표수'] = \
                    self.na.loc[(dong, place), '사전투표수'] * dong_pre_in_ratio
        self.na['관외사전투표수'] = self.na['사전투표수'] - self.na['관내사전투표수']

        self.na['당일투표율'] = self.na['당일투표수'] / self.na['확정된 국내선거인수 (A)'] * 100
        self.na['사전투표율'] = self.na['사전투표수'] / self.na['확정된 국내선거인수 (A)'] * 100
        self.na['관내사전투표율'] = self.na['관내사전투표수'] / self.na['확정된 국내선거인수 (A)'] * 100
        self.na['관내사전투표 비중'] = self.na['관내사전투표수'] / self.na['사전투표수'] * 100
        self.na['투표율'] = self.na['당일투표율'] + self.na['사전투표율']
        self.na['기권율'] = self.na['기권수'] / self.na['확정된 국내선거인수 (A)'] * 100

        self.na.drop(self.na.index[pd.isna(self.na['투표구명'])], axis=0, inplace=True)

    def get_place_pre_score(self):
        self.score.drop(['읍면동투표구명', '대수', '선거명', '선거구명'], axis=1, inplace=True)
        self.score['유형'] = '당일투표'
        score = []

        self.score.set_index(['읍면동명', '투표구명', '유형'], inplace=True)
        for dong in self.dongs:
            dong_pre_score = self.score.loc[(dong, '관내사전투표', '당일투표')].copy()
            dong_pre_sum = dong_pre_score['선거인수']
            for place in self.na.loc[dong].index:
                place_pre_sum = self.na.loc[(dong, place), '관내사전투표수']
                place_pre_score = dong_pre_score / dong_pre_sum * place_pre_sum
                place_pre_score.rename((dong, place, '관내사전투표'), inplace=True)
                score.append(place_pre_score)

        gu_pre_sum = self.na['관외사전투표수'].sum()
        gu_pre_out_score = self.score.loc[('거소·선상투표', '전체', '당일투표')]
        gu_pre_out_score = gu_pre_out_score.add(self.score.loc[('관외사전투표', '전체', '당일투표')])
        if '국외부재자투표' in self.score_dong_unique:
            gu_pre_out_score = gu_pre_out_score.add(self.score.loc[('국외부재자투표', '전체', '당일투표')])
        if '재외투표' in self.score_dong_unique:
            gu_pre_out_score = gu_pre_out_score.add(self.score.loc[('재외투표', '전체', '당일투표')])
        gu_pre_out_score = gu_pre_out_score.add(self.score.loc[('잘못투입·구분된투표지', '전체', '당일투표')])

        for dong in self.dongs:
            for place in self.na.loc[dong].index:
                place_pre_sum = self.na.loc[(dong, place), '관외사전투표수']
                place_pre_score = gu_pre_out_score / gu_pre_sum * place_pre_sum
                place_pre_score.rename((dong, place, '관외사전투표'), inplace=True)
                score.append(place_pre_score)

        self.score = self.score.append(score)
        self.score.drop(['거소·선상투표', '관외사전투표', '국외부재자투표', '재외투표', '잘못투입·구분된투표지'], axis=0, level=0, inplace=True)
        self.score.drop(['소계', '계', '관내사전투표'], axis=0, level=1, inplace=True)
        self.score.sort_index(inplace=True)

    def get_score_analysis(self):
        if '국외부재자투표(공관)' in self.score_dong_unique:
            total_valid = self.score['투표수'].sum() - self.score.loc[('국외부재자투표(공관)', '전체', '당일투표'), '투표수']
        else:
            total_valid = self.score['투표수'].sum()
        stat_score = []
        analysis_total_ratio = []
        analysis_ratio = []
        for dong in self.dongs:
            for place in self.na.loc[dong].index:
                place_score = self.score.loc[(dong, place)]
                score_sum = place_score.sum()
                score_sum.rename((dong, place, '소계'), inplace=True)
        
                score_ratio = score_sum / score_sum['투표수'] * 100
                score_ratio_analysis = score_ratio.copy()
                score_total_ratio_anlaysis = score_sum / total_valid * 100 * self.na.index.size
                score_ratio.rename((dong, place, '비율'), inplace=True)
                score_ratio_analysis.rename((dong, place), inplace=True)
                score_total_ratio_anlaysis.rename((dong, place), inplace=True)
        
                stat_score.append(score_sum)
                stat_score.append(score_ratio)
                analysis_ratio.append(score_ratio_analysis)
                analysis_total_ratio.append(score_total_ratio_anlaysis)
        
        self.score = self.score.append(stat_score)
        self.score.sort_index(inplace=True)
        self.score.to_excel('nec_score.xlsx')
        
        df_ratio = pd.DataFrame(analysis_ratio)
        df_ratio.drop(['선거인수', '투표수'], axis=1, inplace=True)
        df_total_ratio = pd.DataFrame(analysis_total_ratio)
        df_total_ratio.drop(['선거인수', '투표수'], axis=1, inplace=True)
        self.na = pd.concat([self.na, df_ratio], axis=1)
        self.na = pd.concat([self.na, df_total_ratio], axis=1)

    def merge_house_info(self, doc_poll_house_info):
        df_house_infos = pd.read_excel(doc_poll_house_info)
        df_house_info_sub1 = df_house_infos.loc[:, ['투표구명', '세대수', '동수', '전용면적 60이하', '전용면적 60-85이하', '전용면적 85-135이하', '전용면적 135초과', '단지 전용면적합']]
        df_house_info_sub1.rename(columns={'세대수': '공동주택 세대수'}, inplace=True)
        df_house_info_group1 = df_house_info_sub1.groupby('투표구명').sum()
        df_house_info_group2 = df_house_info_sub1.groupby('투표구명').count().copy()
        df_house_info_group2 = df_house_info_group2.loc[:, ['동수']]
        df_house_info_group2.rename(columns={'동수': '공동주택 단지수'}, inplace=True)
        df_house_info_summary = pd.merge(df_house_info_group2, df_house_info_group1, on='투표구명')
        df_house_info_summary.to_excel('group_summary.xlsx')
        
        self.na = pd.merge(self.na, df_house_info_summary, on='투표구명')
        self.na['공동주택 세대수 커버리지'] = self.na['공동주택 세대수'] / self.na['세대수'] * 100
        self.na['세대당 평균 관리비부과면적'] = self.na['단지 전용면적합'] / self.na['공동주택 세대수']

    def run(self, doc_poll_house_info):
        self.get_place_pre_sum()
        self.get_place_pre_score()
        self.get_score_analysis()
        # self.merge_house_info(doc_poll_house_info)
        self.na.to_excel('nec_anlysis.xlsx')
