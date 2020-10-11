from urllib.parse import urlencode, quote_plus
import pandas as pd
import re
from govData import GovData


class HouseDeal(GovData):
    def __init__(self, url, key):
        super().__init__(url, key)

        self._gu_codes = {'기흥구': '41463', '수지구': '41465', '처인구': '41461'}
        self._gu_code = ''
        self._gu_name = ''
        self._deal_ym = ''
        self.deal_type = ''
        if 'SvcApt' in self._callback_url:
            self.house_type = '아파트'
        elif 'SvcRH' in self._callback_url:
            self.house_type = '연립다세대'

    def _set_query_param(self):
        self._query_param = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('LAWD_CD'): self._gu_code, quote_plus('DEAL_YMD'): self._deal_ym})

    def _parse_xml_gu(self):
        self._append_data('구', self._gu_name)
        self._append_data('유형', self.house_type)

    def _get_deal_ym(self, start_year, start_month, end_year, end_month):
        self._deal_yms = []
        for year in range(start_year, end_year+1):
            month0 = 1
            month1 = 12
            if year == start_year:
                month0 = start_month
            if year == end_year:
                month1 = end_month
            for month in range(month0, month1+1):
                ym = str(year) + str(month).zfill(2)
                self._deal_yms.append(ym)

    def get(self, gu_names, start_year, start_month, end_year, end_month):
        self._get_deal_ym(start_year, start_month, end_year, end_month)
        for gu_name in gu_names:
            self._gu_name = gu_name
            self._gu_code = self._gu_codes[gu_name]
            for deal_ym in self._deal_yms:
                print(gu_name, deal_ym)
                self._deal_ym = deal_ym
                self._query()

        self.items = pd.DataFrame(self.data)


class HouseDealTrade(HouseDeal):
    def __init__(self, url, key):
        super().__init__(url, key)

        self.deal_type = 'trade'
        self.data = {
            '년': [],
            '월': [],
            '일': [],
            '단지명': [],
            '구': [],
            '법정동': [],
            '지번': [],
            '건축년도': [],
            '전용면적': [],
            '층': [],
            '유형': [],
            '거래금액': []
        }

    def _parse_xml(self):
        items = self._soup.find_all('item')
        for item in items:
            self._parse_xml_gu()

            split_item = re.split('<.*?>', item.text)
            self._append_data('거래금액', split_item[1].replace(',', ''))
            self._append_data('건축년도', split_item[2])
            self._append_data('년', split_item[3])
            if self.house_type == '아파트':
                self._append_data('법정동', split_item[4])
                self._append_data('단지명', split_item[5])
                self._append_data('월', split_item[6])
                self._append_data('일', split_item[7])
                self._append_data('전용면적', split_item[8])
                self._append_data('지번', split_item[9])
                self._append_data('층', split_item[11])
            elif self.house_type == '연립다세대':
                self._append_data('법정동', split_item[5])
                self._append_data('단지명', split_item[6])
                self._append_data('월', split_item[7])
                self._append_data('일', split_item[8])
                self._append_data('전용면적', split_item[9])
                self._append_data('지번', split_item[10])
                self._append_data('층', split_item[12])


class HouseDealRent(HouseDeal):
    def __init__(self, url, key):
        super().__init__(url, key)

        self.deal_type = 'trade'
        self.data = {
            '년': [],
            '월': [],
            '일': [],
            '단지명': [],
            '구': [],
            '법정동': [],
            '지번': [],
            '건축년도': [],
            '전용면적': [],
            '층': [],
            '유형': [],
            '보증금액': [],
            '월세금액': []
        }

    def _parse_xml(self):
        items = self._soup.find_all('item')
        for item in items:
            self._parse_xml_gu()

            split_item = re.split('<.*?>', item.text)
            self._append_data('건축년도', split_item[1])
            self._append_data('년', split_item[2])
            self._append_data('법정동', split_item[3])
            self._append_data('보증금액', split_item[4].replace(',', ''))
            self._append_data('단지명', split_item[5])
            self._append_data('월', split_item[6])
            self._append_data('월세금액', split_item[7])
            self._append_data('일', split_item[8])
            self._append_data('전용면적', split_item[9])
            self._append_data('지번', split_item[10])
            if len(split_item) > 12:
                self._append_data('층', split_item[12])
            else:
                self._append_data('층', '-')

