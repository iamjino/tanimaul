import pandas as pd

class elecZone:
    def __init__(self):
        self.a = 1
        pass

    def load_detail(self):
        detail_zone = pd.read_excel('conf/용인시 통리반 명칭 및 관할구역.xlsx', sheet_name='step1', index_col=None)
        print(detail_zone.shape)
        temp1 = detail_zone[['개정일', '행정동', '통명', '건물', '법정동', '통', '반', '읍면동', '통리명', '반의명칭', '관할구역']]
        print(temp1)
        print(temp1.shape)

        print(temp1.at[3, '반의명칭'])
        print(temp1.at[4, '반의명칭'])
        temp1 = temp1[temp1['반의명칭'].isna() == False]
        print(temp1.shape)
        temp1 = temp1[temp1['건물'].isna() == False]
        print(temp1.shape)

        temp1['주소'] = ''
        print(temp1.index.size)
        temp3 = temp1.reset_index(drop=True)
        for i in range(temp3.index.size):
            texts = temp3.at[i, '관할구역'].split(' ')
            addr = texts[0] + ' ' + texts[1]
            temp3.at[i, '주소'] = addr

        print(temp3)
        temp3.to_excel('result.xlsx', sheet_name='zone')
        # print(temp1.columns)
        # print(temp1.index)
