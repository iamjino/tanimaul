import pandas as pd


def day_voter(x):
    result = ''
    if x['사전투표수'] > 0:
        result = x['투표수']
    return result


class NecAnalysis():
    def __init__(self, file_result, file_book):
        result_items = pd.read_excel(file_result)
        book_items = pd.read_excel(file_book)

        nec_result_part = result_items[['읍면동투표구명', '읍면동명', '투표구명', '선거인수', '투표수', '기권수']].copy()
        nec_result_part.rename(columns={'읍면동명': '읍면동명_결과', '투표구명': '투표구명_결과'}, inplace=True)
        self.na = pd.merge(book_items, nec_result_part, on='읍면동투표구명', how='right')
        self.score = result_items.copy()
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
                place_pre_score = dong_pre_score * (place_pre_sum / dong_pre_sum)
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
                place_pre_score = gu_pre_out_score * (place_pre_sum / gu_pre_sum)
                place_pre_score.rename((dong, place, '관외사전투표'), inplace=True)
                score.append(place_pre_score)

        self.score = self.score.append(score)
        self.score.rename({'무효 투표수': '무효 투표', '기권수': '기권'}, axis='columns', inplace=True)
        self.score.drop(['거소·선상투표', '관외사전투표', '국외부재자투표', '재외투표', '잘못투입·구분된투표지'], axis=0, level=0, inplace=True)
        self.score.drop(['소계', '계', '관내사전투표'], axis=0, level=1, inplace=True)
        self.score.sort_index(inplace=True)

    def copy_series(self, org_list, dong, place):
        new_list = org_list.copy()
        new_list.rename((dong, place), inplace=True)
        return new_list

    def concat_list(self, add_list):
        df_list = pd.DataFrame(add_list)
        df_list.drop(['선거인수', '투표수'], axis=1, inplace=True)
        self.na = pd.concat([self.na, df_list], axis=1)

    def get_score_analysis(self):
        if '국외부재자투표(공관)' in self.score_dong_unique:
            total_valid = self.score['투표수'].sum() - self.score.loc[('국외부재자투표(공관)', '전체', '당일투표'), '투표수']
        else:
            total_valid = self.score['투표수'].sum()
        stat_score = []
        analysis_total_ratio = []

        ratio_sums = []
        ratio_pres = []
        ratio_days = []
        for dong in self.dongs:
            for place in self.na.loc[dong].index:
                place_score = self.score.loc[(dong, place)]
                score_sum = place_score.sum()
                score_sum.rename((dong, place, '소계'), inplace=True)
                stat_score.append(score_sum)
                total_vote = score_sum['투표수']

                ratio_sum = score_sum / total_vote * 100
                ratio_sum.rename((dong, place, '비율'), inplace=True)
                stat_score.append(ratio_sum)

                score_pre = self.score.loc[(dong, place, ['관내사전투표', '관외사전투표'])].sum()
                score_pre.rename((dong, place, '사전소계'), inplace=True)
                stat_score.append(score_pre)
                ratio_pre = score_pre / total_vote * 100
                ratio_pre.rename((dong, place, '사전비율'), inplace=True)
                stat_score.append(ratio_pre)

                score_day = self.score.loc[(dong, place, ['당일투표'])].sum()
                ratio_day = score_day / total_vote * 100
                ratio_day.rename((dong, place, '당일비율'), inplace=True)
                stat_score.append(ratio_day)

                ratio_sums.append(self.copy_series(ratio_sum, dong, place))
                ratio_pres.append(self.copy_series(ratio_pre, dong, place))
                ratio_days.append(self.copy_series(ratio_day, dong, place))

                score_total_ratio_anlaysis = score_sum / total_valid * 100 * self.na.index.size
                score_total_ratio_anlaysis.rename((dong, place), inplace=True)
                analysis_total_ratio.append(score_total_ratio_anlaysis)

        self.score = self.score.append(stat_score)
        self.score.sort_index(inplace=True)

        self.concat_list(ratio_sums)
        self.concat_list(ratio_pres)
        self.concat_list(ratio_days)

    def merge_house_info(self, sg_id, doc_poll_house_info):
        df_house_infos = pd.read_excel(doc_poll_house_info)
        df_house_info_sub1 = df_house_infos.loc[:, [sg_id, '세대수', '동수', '전용면적 60이하', '전용면적 60-85이하', '전용면적 85-135이하', '전용면적 135초과', '단지 전용면적합']]
        df_house_info_sub1.rename(columns={'세대수': '공동주택 세대수'}, inplace=True)
        df_house_info_summary = df_house_info_sub1.groupby(sg_id).sum()
        df_house_info_summary.insert(0, '공동주택 단지수', df_house_info_sub1.groupby(sg_id).size())
        self.na = pd.merge(self.na, df_house_info_summary, left_on='투표구명', right_index=True, how='left')
        self.na['세대 평균 전용면적'] = self.na['단지 전용면적합'] / self.na['공동주택 세대수']
        self.na['공동주택 세대수 커버리지'] = self.na['공동주택 세대수'] / self.na['세대수'] * 100

    def run(self, sg_id, doc_poll_house_info):
        self.get_place_pre_sum()
        self.get_place_pre_score()
        self.merge_house_info(sg_id, doc_poll_house_info)
        self.get_score_analysis()
