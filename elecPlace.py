import pandas as pd

class ElecPlace:
    def __init__(self):
        self.df = pd.read_excel('conf/투표구 관할구역(용인시정).xlsx', sheet_name='2020년 제21대 국회의원선거', skiprows=2)

    def decode(self):
        key_gu = '구·시·군명'
        key_place = '투표소명'
        key_region = '투표구 관할구역'
        key_place_dong = '투표소 동'
        key_dong = '투표구 동'
        key_tong = '투표구 통'
        infos = {key_gu: [], key_place: [], key_place_dong: [], key_dong: [], key_tong: []}
        for index in range(len(self.df)):
            # one_row = self.df.iloc[[index], :]
            # value_gu = one_row[key_gu].values[0]
            # value_place = one_row[key_place].values[0]
            # value_regions = one_row[key_region].values[0].split('/')
            value_gu = self.df.iloc[index][0]
            value_place = self.df.iloc[index][1]
            value_place_dong = value_place.split('제')[0]
            value_regions = self.df.iloc[index][2].split('/')
            for value_region in value_regions:
                addr = value_region.strip()
                value_dong = addr.split(' ')[0]
                addr = addr.replace(value_dong, '', 1)
                addr = addr.replace(' ', '')
                addr = addr.replace('통', '')
                addr = addr.replace('∼', '~')
                tongs = addr.split(',')
                for tong in tongs:
                    if tong.find('~') != -1:
                        tong_limit = tong.split('~')
                    else:
                        tong_limit = [tong, tong]
                    tong_range = range(int(tong_limit[0]), int(tong_limit[1])+1)
                    for value_tong in tong_range:
                        infos[key_gu].append(value_gu)
                        infos[key_place].append(value_place)
                        infos[key_place_dong].append(value_place_dong)
                        infos[key_dong].append(value_dong)
                        infos[key_tong].append(value_tong)

        self.items = pd.DataFrame(infos)
