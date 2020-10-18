import pandas as pd

class NecPollHouse:
    def __init__(self, conf_yiaddr_file, conf_yiaddr_sheet, conf_yiaddr_file_fix, doc_house_info, doc_poll_addr_list):
        self._house_info = pd.read_excel(doc_house_info)
        self._poll_addr = pd.read_excel(doc_poll_addr_list)
        self.conf_yiaddr_file = conf_yiaddr_file
        self.conf_yiaddr_sheet = conf_yiaddr_sheet
        self.conf_yiaddr_file_fix = conf_yiaddr_file_fix
        pass

    def run(self):
        yi_zone = pd.read_excel(self.conf_yiaddr_file, sheet_name=self.conf_yiaddr_sheet, index_col=None)
        temp1 = yi_zone[['개정일', '행정동', '통명', '건물', '법정동', '통', '반', '읍면동', '통리명', '반의명칭', '관할구역']]
        temp1 = temp1[temp1['반의명칭'].notnull()]
        temp1 = temp1[temp1['건물'].notnull()]

        yi_zone_fix = pd.read_excel(self.conf_yiaddr_file_fix, index_col=None)
        addr_replace = yi_zone_fix[yi_zone_fix['타입'] == 'replace'].reset_index(drop=True)
        addr_change = yi_zone_fix[yi_zone_fix['타입'] == 'change'].reset_index(drop=True)
        house_addr = temp1.reset_index(drop=True)
        for i in range(house_addr.index.size):
            text = house_addr.at[i, '관할구역']
            text = text.replace('(', ' ')
            text = text.replace(')', ' ')
            text = text.replace('   ', ' ')
            text = text.replace('  ', ' ')

            for j in range(addr_change.index.size):
                addrs = text.split(' ')
                if len(addrs) > 2:
                    is_match1 = addrs[0] == addr_change.at[j, '단어1']
                    is_match3 = addrs[2] == addr_change.at[j, '단어3']
                    if is_match1 & is_match3:
                        addrs[1] = addr_change.at[j, '단어2']
                        text = ' '.join(addrs)

            for j in range(addr_replace.index.size):
                text = text.replace(addr_replace.at[j, '을'], addr_replace.at[j, '으로'])

            house_addr.at[i, '관할구역'] = text

        temp1['주소'] = ''
        dong_changes = ['죽전1동', '상현2동']
        for i in range(house_addr.index.size):
            text = house_addr.at[i, '관할구역']
            addrs = text.split(' ')
            addr = addrs[0] + ' ' + addrs[1]
            house_addr.at[i, '주소'] = addr

            house_addr.at[i, '법정동'] = house_addr.at[i, '법정동'] + '동'
            for dong_change in dong_changes:
                if house_addr.at[i, '행정동'] == dong_change:
                    house_addr.at[i, '법정동'] = dong_change

        house_addr['투표구명'] = ''
        for i in range(house_addr.index.size):
            is_dong = self._poll_addr['법정동'] == house_addr.at[i, '법정동']
            is_tong = self._poll_addr['통'] == house_addr.at[i, '통']
            df_place = self._poll_addr[is_dong & is_tong].reset_index(drop=True)
            if df_place.size > 0:
                house_addr.at[i, '투표구명'] = df_place.at[0, '투표구명']

        house_addr['단지명'] = ''
        for i in range(house_addr.index.size):
            addr = house_addr.at[i, '주소']
            is_addr = self._house_info['동이하주소'] == addr
            df_apt = self._house_info[is_addr].reset_index(drop=True)
            if df_apt.size > 0:
                house_addr.at[i, '단지명'] = df_apt.at[0, '단지명']

        house_addr.to_excel('doc/임시-통리반 관할구역.xlsx', sheet_name='zone')

        concise_addr = house_addr[['행정동', '법정동', '투표구명', '단지명', '주소']]
        concise_addr = concise_addr[concise_addr['단지명'] != '']
        self.items = concise_addr.drop_duplicates(subset=['단지명'], ignore_index=True)
        print(self.items)

    def to_excel(self, xlsx_name, sheet_name='sheet1'):
        self.items.to_excel(xlsx_name, sheet_name=sheet_name)
