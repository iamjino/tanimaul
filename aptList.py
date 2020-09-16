from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd


class AptList:
    def __init__(self,  key):
        self.items = ''
        self._dong_names = []
        self._kapt_codes = []
        self._kapt_names = []
        self._callback_url = 'http://apis.data.go.kr/1611000/AptListService/getLegaldongAptList'
        self._service_key = key

    def _create_url(self):
        query_params = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('bjdCode'): self._bjd_code, quote_plus('numOfRows'): '100'})
        self._url = self._callback_url + query_params

    def _request(self):
        request = Request(self._url)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        self._soup = BeautifulSoup(response_body, 'html.parser')

    def _parse_xml(self):
        # self._pretty_soup = self._soup.prettify()
        items = self._soup.find_all('item')
        for item in items:
            self._dong_names.append(self._dong_name)
            self._kapt_codes.append(item.find('kaptcode').string)
            self._kapt_names.append(item.find('kaptname').string)

    def _query(self, bjd_code, dong_name):
        self._bjd_code = bjd_code
        self._dong_name = dong_name
        self._create_url()
        self._request()
        self._parse_xml()

    def _get_bjd_code(self, bjd_file):
        bjd_code_df = pd.read_csv(bjd_file, sep='\t', encoding='EUC-KR')
        bjd_code_df.columns = ['bjd_code', 'dong_name', 'valid']
        bjd_code_df.columns.name = 'Code Info'

        self._bjd_code_df = bjd_code_df.loc[bjd_code_df['valid'] == '존재', :]

    def get(self, bjd_file, target_gus, target_dongs):
        self._get_bjd_code(bjd_file)
        for index, dong_name_full in enumerate(self._bjd_code_df['dong_name']):
            gu_name = dong_name_full.split(' ')[2]
            dong_name = dong_name_full.split(' ')[-1]
            is_query = False
            if len(target_gus) > 0:
                if gu_name in target_gus:
                    is_query = True
            else:
                if dong_name in target_dongs:
                    is_query = True

            if is_query:
                bjd_code = self._bjd_code_df['bjd_code'].iloc[index]
                self._query(bjd_code, dong_name)

        self.items = pd.DataFrame({'단지코드': self._kapt_codes, '단지명': self._kapt_names, '법정': self._dong_names})
