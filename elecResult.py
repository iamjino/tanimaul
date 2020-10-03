import pandas as pd

class ElecResult:
    def __init__(self):

        pass

    def run(self):
        df = pd.read_excel('doc/통리반 관할구역.xlsx', sheet_name='zone')
        places = {
            '구성동제1투',
            '구성동제2투',
            '구성동제3투',
            '구성동제4투',
            '구성동제5투',
            '구성동제6투',
            '구성동제7투',
            '구성동제8투',
            '마북동제1투',
            '마북동제2투',
            '마북동제3투',
            '마북동제4투',
            '마북동제5투',
            '마북동제6투',
            '마북동제7투',
            '동백1동제1투',
            '동백1동제2투',
            '동백1동제3투',
            '동백1동제4투',
            '동백1동제5투',
            '동백1동제6투',
            '동백2동제1투',
            '동백2동제2투',
            '동백2동제3투',
            '동백2동제4투',
            '동백2동제5투',
            '보정동제1투',
            '보정동제2투',
            '보정동제3투',
            '보정동제4투',
            '보정동제5투',
            '보정동제6투',
            '보정동제7투',
            '죽전1동제1투',
            '죽전1동제2투',
            '죽전1동제3투',
            '죽전1동제4투',
            '죽전1동제5투',
            '죽전1동제6투',
            '죽전1동제7투',
            '죽전1동제8투',
            '죽전1동제9투',
            '죽전1동제10투',
            '상현2동제1투',
            '상현2동제2투',
            '상현2동제3투',
            '상현2동제4투',
            '상현2동제5투',
            '상현2동제6투'
        }
        # for place in places:
        #     place_loc = df[df['투표소명'] == place]
        #     grouped = place_loc.groupby(place_loc['단지명'])
        #     print(place, grouped.count().index.tolist())
        #     print(place_loc.columns)

        df_summary = df[['투표소명', '단지명', '주소']]
        df_summary = df_summary[df_summary['단지명'].notnull()]
        df_concise = df_summary.drop_duplicates(subset=['단지명'], ignore_index=True)
        print(df_concise)
        df_concise.to_excel('result.xlsx')
