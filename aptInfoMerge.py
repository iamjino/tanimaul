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

        self.yicity['도로명주소'] = self.yicity['도로명주소'].fillna('')
        self.yicity['간략 도로명주소'] = self.yicity['도로명주소'].str.strip()
        # self.yicity['간략 도로명주소'] = self.yicity['도로명주소'].str.split('(').get(0).strip()
        size = self.yicity.index.size;
        for i in range(size):
            self.yicity.at[i, '간략 도로명주소'] = self.yicity.at[i, '도로명주소'].split('(')[0].strip()
        self.yicity['doraddr'] = self.yicity['간략 도로명주소'].str.replace(' ', '')
        print('yicity:', self.yicity.index.size)

    def load_kapt(self):
        self.kapt = pd.read_excel('공동주택 현황.xlsx', sheet_name='code')
        bugfix = pd.read_excel('conf/공동주택 현황-KAPT 수정.xlsx', sheet_name='apt')
        for b in range(bugfix.index.size):
            code = bugfix.at[b, '단지코드']
            indexes = self.kapt.index[self.kapt['단지코드'] == code]
            if indexes.size > 0:
                index = indexes[0]
                print(index)
                self.kapt.at[index, '법정동주소'] = bugfix.at[b, '법정동주소']
                self.kapt.at[index, '도로명주소'] = bugfix.at[b, '도로명주소']
                self.kapt.at[index, '단지명'] = bugfix.at[b, '단지명']

        self.kapt['간략 법정동주소'] = self.kapt['법정동주소'].str.replace('경기도 용인시 ', '')
        self.kapt['간략 도로명주소'] = self.kapt['도로명주소'].str.replace('경기도 용인시 ', '')
        self.kapt['bjdaddr'] = self.kapt['간략 법정동주소'].str.replace(' ', '')
        self.kapt['doraddr'] = self.kapt['간략 도로명주소'].str.replace(' ', '')
        print('kapt:', self.kapt.index.size)

        self.merged = self.kapt.copy()
        self.merged['용인시 법정동주소'] = ''
        self.merged['용인시 도로명주소'] = ''
        self.merged['용인시 불일치'] = ''
        self.merged['용인시 세대수'] = ''
        self.merged['세대수 차이'] = ''
        self.merged['용인시 단지명'] = ''

        print(self.merged)

    def run(self):
        bothmatch = 0
        dormatch = 0
        bjdmatch = 0
        nomatch = 0
        for y in range(self.yicity.index.size):
            yicity_dor = self.yicity.at[y, 'doraddr']
            yicity_bjd = self.yicity.at[y, 'bjdaddr']
            yicity_cnt = self.yicity.at[y, '세대수']
            dor = False
            bjd = False
            k_index = 0

            for k in range(self.kapt.index.size):
                kapt_dor = self.kapt.at[k, 'doraddr']
                kapt_bjd = self.kapt.at[k, 'bjdaddr']
                if not dor:
                    if kapt_dor == yicity_dor:
                        if self.merged.at[k, '용인시 불일치'] == '':
                            dor = True
                            k_index = k
                if not bjd:
                    if kapt_bjd == yicity_bjd:
                        if self.merged.at[k, '용인시 불일치'] == '':
                            bjd = True
                            k_index = k

            yicity_name = self.yicity.at[y, '단지명'].strip()
            yicity_bjdaddr = self.yicity.at[y, '간략 법정동주소'].strip()
            yicity_doraddr = self.yicity.at[y, '간략 도로명주소'].strip()
            if dor or bjd:
                self.merged.at[k_index, '용인시 단지명'] = yicity_name
                self.merged.at[k_index, '용인시 법정동주소'] = yicity_bjdaddr
                self.merged.at[k_index, '용인시 도로명주소'] = yicity_doraddr
                self.merged.at[k_index, '용인시 세대수'] = yicity_cnt
                if self.merged.at[k_index, '세대수'] != yicity_cnt:
                    self.merged.at[k_index, '세대수 차이'] = self.merged.at[k_index, '세대수'] - yicity_cnt

                if dor and bjd:
                    bothmatch += 1
                    self.merged.at[k_index, '용인시 불일치'] = '주소 모두 일치'
                elif dor:
                    dormatch += 1
                    self.merged.at[k_index, '용인시 불일치'] = '법정동주소 불일치'
                else:
                    bjdmatch += 1
                    self.merged.at[k_index, '용인시 불일치'] = '도로명주소 불일치'
            else:
                nomatch += 1
                yicity_bjdfull = '경기도 용인시 ' + yicity_bjdaddr
                yicity_dorfull = '경기도 용인시 ' + yicity_doraddr

                yicity_tel = self.yicity.at[y, '관리사무소 전화번호']
                yicity_sale = self.yicity.at[y, '분양형태'].strip()
                self.merged = self.merged.append({'용인시 법정동주소': yicity_bjdaddr,
                                                  '용인시 도로명주소': yicity_doraddr,
                                                  'bjdaddr': yicity_bjd,
                                                  'doraddr': yicity_dor,
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

        print(bothmatch, dormatch, bjdmatch, nomatch)
        self.merged.to_excel('공동주택 현황(병합).xlsx', sheet_name='apt')
