from urllib.parse import urlencode, quote_plus
import pandas as pd
from govData import GovData


class KaptList(GovData):
    def __init__(self,  key):
        oldurl = 'http://apis.data.go.kr/1611000/AptListService/getLegaldongAptList'
        url = 'http://apis.data.go.kr/1613000/AptListService1/getLegaldongAptList'
        super(self.__class__, self).__init__(url, key)

        self._bjd_code = ''
        self._dong_name = ''
        self.data = {
            '단지코드': [],
            '법정동': []
        }

    def _set_query_param(self):
        self._query_param = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('bjdCode'): self._bjd_code, quote_plus('numOfRows'): '100'})

    def _parse_xml(self):
        items = self._soup.find_all('item')
        for item in items:
            self._append_data('법정동', self._dong_name)
            self._parse_xml_line(item, '단지코드', 'kaptcode')

    def get(self, bjd_codes, target_gus, target_dongs):
        for index, dong_name_full in enumerate(bjd_codes['dong_name']):
            gu_name = dong_name_full.split(' ')[2]
            self._dong_name = dong_name_full.split(' ')[-1]
            is_query = False
            if len(target_gus) > 0:
                if gu_name in target_gus:
                    is_query = True
            elif len(target_dongs) > 0:
                if self._dong_name in target_dongs:
                    is_query = True

            if is_query:
                self._bjd_code = bjd_codes['bjd_code'].iloc[index]
                self._query()

        self.items = pd.DataFrame(self.data)
