import pandas as pd

class elecZone:
    def __init__(self):
        self._elec_place = pd.read_excel('투표구 관할구역.xlsx', sheet_name='place')
        pass

    def load_detail(self):
        raw_zone = pd.read_excel('conf/용인시 통리반 관할구역.xlsx', sheet_name='step1', index_col=None)
        print(raw_zone.shape)
        temp1 = raw_zone[['개정일', '행정동', '통명', '건물', '법정동', '통', '반', '읍면동', '통리명', '반의명칭', '관할구역']]
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
        tong_addr = temp1.reset_index(drop=True)
        dong_changes = ['죽전1동', '상현2동']
        for i in range(tong_addr.index.size):
            texts = tong_addr.at[i, '관할구역'].split(' ')
            addr = texts[0] + ' ' + texts[1]
            tong_addr.at[i, '주소'] = addr
            tong_addr.at[i, '법정동'] = tong_addr.at[i, '법정동'] + '동'
            for dong_change in dong_changes:
                if tong_addr.at[i, '행정동'] == dong_change:
                    tong_addr.at[i, '법정동'] = dong_change

        print(tong_addr)
        tong_addr['투표소명'] = ''
        for i in range(tong_addr.index.size):
            dong = self._elec_place['법정동'] == tong_addr.at[i, '법정동']
            tong = self._elec_place['통'] == tong_addr.at[i, '통']
            df_place = self._elec_place[dong & tong].reset_index(drop=True)
            if(df_place.size > 0):
                tong_addr.at[i, '투표소명'] = df_place.at[0, '투표소명']
        tong_addr.to_excel('result.xlsx', sheet_name='zone')
