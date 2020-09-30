import pandas as pd

class AptInfoMerge:
    def __init__(self):
        self.load_yicity()
        self.load_kapt()

    def load_yicity(self):
        self.yicity = pd.read_excel('conf/용인시 공동주택 현황.xlsx', sheet_name='summary')
        self.yicity['간략 법정동주소'] = self.yicity["법정동주소"].str.replace(pat="1동", repl="동")
        self.yicity['간략 법정동주소'] = self.yicity['간략 법정동주소'].str.replace(pat="2동", repl="동")
        self.yicity['간략 법정동주소'] = self.yicity['간략 법정동주소'].str.strip()
        self.yicity['bjdaddr'] = self.yicity['간략 법정동주소'].str.replace(' ', '')
        # print(self.yicity['bjdaddr'])

        self.yicity['도로명주소'] = self.yicity['도로명주소'].fillna('')
        self.yicity['간략 도로명주소'] = self.yicity['도로명주소'].str.strip()
        # self.yicity['간략 도로명주소'] = self.yicity['도로명주소'].str.split('(').get(0).strip()
        size = self.yicity.index.size;
        for i in range(size):
            self.yicity.at[i, '간략 도로명주소'] = self.yicity.at[i, '도로명주소'].split('(')[0].strip()
        self.yicity['doraddr'] = self.yicity['간략 도로명주소'].str.replace(' ', '')
        # print(self.yicity['doraddr'])

    def load_kapt(self):
        self.kapt = pd.read_excel('공동주택 현황.xlsx', sheet_name='code')
        self.kapt['bjdaddr'] = self.kapt['간략 법정동주소'].str.replace(' ', '')
        self.kapt['doraddr'] = self.kapt['간략 도로명주소'].str.replace(' ', '')
        self.merged = self.kapt.copy()
        self.merged['용인시 법정동주소'] = ''
        self.merged['용인시 도로명주소'] = ''
        self.merged['용인시 불일치'] = ''
        self.merged['용인시 단지명'] = ''
        print(self.merged)

    def run(self):
        # self.items = pd.merge(self.kapt, self.yicity, on=['doroaddr'], how="outer")
        # self.items.to_excel('공동주택 현황(병합).xlsx', sheet_name='apt')
        # print(self.items)
        # bjd 643 doro 629

        bothmatch = 0
        dormatch = 0
        bjdmatch = 0
        nomatch = 0
        for y in range(self.yicity.index.size):
            yicity_dor = self.yicity.at[y, 'doraddr']
            yicity_bjd = self.yicity.at[y, 'bjdaddr']
            yicity_name = self.yicity.at[y, '단지명'].strip()
            dor = False
            bjd = False
            k_index = 0
            for k in range(self.kapt.index.size):
                kapt_dor = self.kapt.at[k, 'doraddr']
                kapt_bjd = self.kapt.at[k, 'bjdaddr']

                if not dor:
                    if kapt_dor == yicity_dor:
                        dor = True
                        k_index = k
                if not bjd:
                    if kapt_bjd == yicity_bjd:
                        bjd = True
                        k_index = k

            if dor and bjd:
                # print('exact')
                bothmatch += 1
                self.merged.at[k_index, '용인시 법정동주소'] = yicity_bjd
                self.merged.at[k_index, '용인시 도로명주소'] = yicity_dor
                self.merged.at[k_index, '용인시 단지명'] = yicity_name
                self.merged.at[k_index, '용인시 불일치'] = '일치'
            elif dor:
                # print('dor')
                dormatch += 1
                self.merged.at[k_index, '용인시 법정동주소'] = yicity_bjd
                self.merged.at[k_index, '용인시 도로명주소'] = yicity_dor
                self.merged.at[k_index, '용인시 단지명'] = yicity_name
                self.merged.at[k_index, '용인시 불일치'] = '법정동주소 불일치'
            elif bjd:
                # print('bjd')
                bjdmatch += 1
                self.merged.at[k_index, '용인시 법정동주소'] = yicity_bjd
                self.merged.at[k_index, '용인시 도로명주소'] = yicity_dor
                self.merged.at[k_index, '용인시 단지명'] = yicity_name
                self.merged.at[k_index, '용인시 불일치'] = '도로명주소 불일치'
            else:
                nomatch += 1
                yicity_bjdaddr = self.yicity.at[y, '간략 법정동주소'].strip()
                yicity_doraddr = self.yicity.at[y, '간략 도로명주소'].strip()

                yicity_cnt = self.yicity.at[y, '세대수']
                yicity_tel = self.yicity.at[y, '관리사무소 전화번호']
                yicity_sale = self.yicity.at[y, '분양형태'].strip()
                self.merged = self.merged.append({'용인시 법정동주소':yicity_bjd,
                                                  '용인시 도로명주소':yicity_dor,
                                                  'bjdaddr':yicity_bjd,
                                                  'doraddr':yicity_dor,
                                                  '간략 법정동주소': yicity_bjdaddr,
                                                  '간략 도로명주소': yicity_doraddr,
                                                  '단지명': yicity_name,
                                                  '분양형태': yicity_sale,
                                                  '세대수': yicity_cnt,
                                                  '관리사무소 연락처': yicity_tel
                                                  }, ignore_index=True)

        print(bothmatch, dormatch, bjdmatch, nomatch)
        self.merged.to_excel('공동주택 현황(병합).xlsx', sheet_name='apt')
