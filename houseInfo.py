import pandas as pd


class HouseInfo:
    def __init__(self, conf_yiapt_list_file, conf_yiapt_list_sheet, doc_kapt_info, conf_kapt_info_fix):
        self._load_yicity(conf_yiapt_list_file, conf_yiapt_list_sheet)
        self._load_kapt(doc_kapt_info, conf_kapt_info_fix)

    def _load_yicity(self, conf_yiapt_list_file, conf_yiapt_list_sheet):
        self.yicity = pd.read_excel(conf_yiapt_list_file, sheet_name=conf_yiapt_list_sheet)

        self.yicity['간략 법정동주소'] = self.yicity["법정동주소"].str.replace(pat="1동", repl="동")
        self.yicity['간략 법정동주소'] = self.yicity['간략 법정동주소'].str.replace(pat="2동", repl="동")
        self.yicity['간략 법정동주소'] = self.yicity['간략 법정동주소'].str.strip()
        self.yicity['bjdkey'] = self.yicity['간략 법정동주소'].str.replace(' ', '')

        self.yicity['도로명주소'] = self.yicity['도로명주소'].fillna('')
        self.yicity['간략 도로명주소'] = self.yicity['도로명주소'].str.strip()
        for i in range(self.yicity.index.size):
            self.yicity.at[i, '간략 도로명주소'] = self.yicity.at[i, '도로명주소'].split('(')[0].strip()
        self.yicity['dorokey'] = self.yicity['간략 도로명주소'].str.replace(' ', '')

    def _load_kapt(self, doc_kapt_info, conf_kapt_info_fix):
        self.kapt = pd.read_excel(doc_kapt_info)
        bugfix = pd.read_excel(conf_kapt_info_fix)
        for b in range(bugfix.index.size):
            code = bugfix.at[b, '단지코드']
            indexes = self.kapt.index[self.kapt['단지코드'] == code]
            if indexes.size > 0:
                self.kapt.at[indexes[0], '법정동주소'] = bugfix.at[b, '법정동주소']
                self.kapt.at[indexes[0], '도로명주소'] = bugfix.at[b, '도로명주소']
                self.kapt.at[indexes[0], '단지명'] = bugfix.at[b, '단지명']

        self.kapt['간략 법정동주소'] = self.kapt['법정동주소'].str.replace('경기도 용인시 ', '')
        self.kapt['간략 도로명주소'] = self.kapt['도로명주소'].str.replace('경기도 용인시 ', '')
        self.kapt['bjdkey'] = self.kapt['간략 법정동주소'].str.replace(' ', '')
        self.kapt['dorokey'] = self.kapt['간략 도로명주소'].str.replace(' ', '')
        self.kapt['동이하주소'] = ''

        self.items = self.kapt.copy()
        self.items['용인시 법정동주소'] = ''
        self.items['용인시 도로명주소'] = ''
        self.items['용인시 불일치'] = ''
        self.items['용인시 세대수'] = ''
        self.items['세대수 차이'] = ''
        self.items['용인시 단지명'] = ''

    def run(self):
        self._bothmatch = 0
        self._doromatch = 0
        self._bjdmatch = 0
        self._nomatch = 0
        for y in range(self.yicity.index.size):
            yicity_dor = self.yicity.at[y, 'dorokey']
            yicity_bjd = self.yicity.at[y, 'bjdkey']
            yicity_cnt = self.yicity.at[y, '세대수']
            dor = False
            bjd = False
            k_index = 0

            for k in range(self.kapt.index.size):
                kapt_dor = self.kapt.at[k, 'dorokey']
                kapt_bjd = self.kapt.at[k, 'bjdkey']
                if not dor:
                    if kapt_dor == yicity_dor:
                        if self.items.at[k, '용인시 불일치'] == '':
                            dor = True
                            k_index = k
                if not bjd:
                    if kapt_bjd == yicity_bjd:
                        if self.items.at[k, '용인시 불일치'] == '':
                            bjd = True
                            k_index = k

            yicity_name = self.yicity.at[y, '단지명'].strip()
            yicity_bjdaddr = self.yicity.at[y, '간략 법정동주소'].strip()
            yicity_doraddr = self.yicity.at[y, '간략 도로명주소'].strip()
            if dor or bjd:
                self.items.at[k_index, '용인시 단지명'] = yicity_name
                self.items.at[k_index, '용인시 법정동주소'] = yicity_bjdaddr
                self.items.at[k_index, '용인시 도로명주소'] = yicity_doraddr
                self.items.at[k_index, '용인시 세대수'] = yicity_cnt
                if self.items.at[k_index, '세대수'] != yicity_cnt:
                    self.items.at[k_index, '세대수 차이'] = self.items.at[k_index, '세대수'] - yicity_cnt

                if dor and bjd:
                    self._bothmatch += 1
                    self.items.at[k_index, '용인시 불일치'] = '주소 모두 일치'
                elif dor:
                    self._doromatch += 1
                    self.items.at[k_index, '용인시 불일치'] = '법정동주소 불일치'
                else:
                    self._bjdmatch += 1
                    self.items.at[k_index, '용인시 불일치'] = '도로명주소 불일치'
            else:
                self._nomatch += 1
                yicity_bjdfull = '경기도 용인시 ' + yicity_bjdaddr
                yicity_dorfull = '경기도 용인시 ' + yicity_doraddr

                yicity_tel = self.yicity.at[y, '관리사무소 전화번호']
                yicity_sale = self.yicity.at[y, '분양형태'].strip()
                self.items = self.items.append({'용인시 법정동주소': yicity_bjdaddr,
                                                  '용인시 도로명주소': yicity_doraddr,
                                                  'bjdkey': yicity_bjd,
                                                  'dorokey': yicity_dor,
                                                  '간략 법정동주소': yicity_bjdaddr,
                                                  '간략 도로명주소': yicity_doraddr,
                                                  '법정동주소': yicity_bjdfull,
                                                  '도로명주소': yicity_dorfull,
                                                  '단지명': yicity_name,
                                                  '용인시 단지명': yicity_name,
                                                  '분양형태': yicity_sale,
                                                '세대수': yicity_cnt,
                                                '관리사무소 연락처': yicity_tel
                                                }, ignore_index=True)

        for k in range(self.items.index.size):
            addrs = self.items.at[k, '간략 법정동주소'].split(' ')
            del addrs[0]
            text = ' '.join(addrs)
            self.items.at[k, '동이하주소'] = text

    def print(self):
        print('용인시 제공 공동주택 단지수:', self.yicity.index.size)
        print('KAPT에서 입수한 공동주택 단지수:', self.kapt.index.size)
        print('공동주택 현황 병합 결과 전체 단지수:', self.items.index.size)
        print(' - 법정동주소와 도로명주소 일치하는 단지수:', self._bothmatch)
        print(' - 법정동주소만 일치하는 단지수:', self._bjdmatch)
        print(' - 도로명주소만 일치하는 단지수:', self._doromatch)
        print(' - 주소가 일치하지 않는 단지수:', self._nomatch)

    def to_excel(self, xlsx_name, sheet_name='sheet1'):
        self.items.to_excel(xlsx_name, sheet_name=sheet_name)
