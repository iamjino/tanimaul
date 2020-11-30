import pandas as pd

class NecZoneHouse:
    def __init__(self, law_addr_file, law_addr_sheet, law_addr_file_fix, doc_house_info, doc_zone_addr_list):
        self._house_info = pd.read_excel(doc_house_info)
        self._zone_addr = pd.read_excel(doc_zone_addr_list)
        self.law_addr_file = law_addr_file
        self.law_addr_sheet = law_addr_sheet
        self.law_addr_file_fix = law_addr_file_fix
        pass

    def run(self):
        df_temp = pd.read_excel(self.law_addr_file, sheet_name=self.law_addr_sheet, index_col=None)
        temp1 = df_temp[['행정동', '통명', '건물', '법정동', '통', '반', '읍면동', '통리명', '반의명칭', '관할구역']]
        temp1 = temp1[temp1['반의명칭'].notnull()]
        temp1 = temp1[temp1['통'].notnull()]
        self.law_addr = temp1.reset_index(drop=True)

        df_law_addr_fix = pd.read_excel(self.law_addr_file_fix, index_col=None)
        addr_replace = df_law_addr_fix[df_law_addr_fix['타입'] == 'replace'].reset_index(drop=True)
        addr_change = df_law_addr_fix[df_law_addr_fix['타입'] == 'change'].reset_index(drop=True)
        for i in range(self.law_addr.index.size):
            text = self.law_addr.at[i, '관할구역']
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

            self.law_addr.at[i, '관할구역'] = text

        temp1['주소'] = ''
        dong_changes = ['죽전1동', '죽전2동', '상현1동', '상현2동', '풍덕천1동', '풍덕천2동']
        for i in range(self.law_addr.index.size):
            text = self.law_addr.at[i, '관할구역']
            addrs = text.strip().split(' ')
            addr = addrs[0] + ' ' + addrs[1]
            self.law_addr.at[i, '주소'] = addr

            self.law_addr.at[i, '법정동'] = self.law_addr.at[i, '법정동'] + '동'
            # self.law_addr.at[i, '행정동'] = self.law_addr.at[i, '행정동'].replace(' ', '')
            # for dong_change in dong_changes:
            #     if self.law_addr.at[i, '행정동'] == dong_change:
            #         self.law_addr.at[i, '법정동'] = dong_change

        self.law_addr['시'] = ''
        self.law_addr['구'] = ''
        self.law_addr['투표구명'] = ''
        self.law_addr['행정동'] = self.law_addr['행정동'].str.replace(' ', '')
        for i in range(self.law_addr.index.size):
            is_hjdong = self._zone_addr['행정동'] == self.law_addr.at[i, '행정동']
            is_bjdong = self._zone_addr['법정동'] == self.law_addr.at[i, '법정동']
            is_tong = self._zone_addr['통'] == self.law_addr.at[i, '통']
            df_place = self._zone_addr[is_hjdong & is_bjdong & is_tong].reset_index(drop=True)
            if df_place.size > 0:
                # self.house_addr.at[i, '시'] = df_place.at[0, '시']
                # self.house_addr.at[i, '구'] = df_place.at[0, '구']
                self.law_addr.at[i, '투표구명'] = df_place.at[0, '투표구명']

        self.law_addr['단지명'] = ''
        for i in range(self.law_addr.index.size):
            addr = self.law_addr.at[i, '주소']
            is_addr = self._house_info['동이하주소'] == addr
            df_apt = self._house_info[is_addr].reset_index(drop=True)
            if df_apt.size > 0:
                texts = df_apt.at[0, '법정동주소'].split(' ')
                self.law_addr.at[i, '시'] = texts[1]
                self.law_addr.at[i, '구'] = texts[2]
                self.law_addr.at[i, '단지명'] = df_apt.at[0, '단지명']

        concise_addr = self.law_addr[['시', '구', '행정동', '법정동', '투표구명', '단지명', '주소']]
        concise_addr = concise_addr[concise_addr['단지명'] != '']
        self.items = concise_addr.drop_duplicates(subset=['단지명'], ignore_index=True)
        print(self.items)

    # def to_excel(self, xlsx_name):
    #     self.items.to_excel(xlsx_name, ignore_index=True)
