import pandas as pd


class NecPollAddress:
    def __init__(self, conf_yi_elecplace_file, conf_yi_elecplace_sheet):
        self.df = pd.read_excel(conf_yi_elecplace_file, sheet_name=conf_yi_elecplace_sheet, skiprows=2)

    def run(self):
        key_gu = '구·시·군명'
        key_place = '투표구명'
        key_region = '투표구 관할구역'
        key_hj_dong = '행정동'
        key_bj_dong = '법정동'
        key_tong = '통'
        infos = {key_gu: [], key_place: [], key_hj_dong: [], key_bj_dong: [], key_tong: []}
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
                        infos[key_hj_dong].append(value_place_dong)
                        infos[key_bj_dong].append(value_dong)
                        infos[key_tong].append(value_tong)

        self.items = pd.DataFrame(infos)

    def to_excel(self, xlsx_name, sheet_name='sheet1'):
        self.items.to_excel(xlsx_name, sheet_name=sheet_name)
