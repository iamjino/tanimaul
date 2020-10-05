from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd
import re

class AptPrice:
    def __init__(self,  key):
        self._callback_url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
        # self._callback_url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
        self._service_key = key
        self._bjd_code_df = {'기흥구': '41463', '수지구': '41465', '처인구': '41461'}
        self.items = ''
        self._dong_names = []
        self._kapt_codes = []
        self._kapt_names = []
        self.infos = {
            '년': [],
            '월': [],
            '일': [],
            '단지명': [],
            '거래금액': [],
            '구': [],
            '법정동': [],
            '지번': [],
            '건축년도': [],
            '전용면적': [],
            '층': []
        }

    def _create_url(self):
        query_params = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('LAWD_CD'): self._land_code, quote_plus('DEAL_YMD'): self._deal_ymd})
        self._url = self._callback_url + query_params

    def _request(self):
        request = Request(self._url)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        self._soup = BeautifulSoup(response_body, 'html.parser')

    def _append_info(self, key, value):
        if isinstance(value, type(None)):
            value = ''
        else:
            value = value.strip()
        self.infos[key].append(value)

    def _parse_xml(self, land_name):
        # self._pretty_soup = self._soup.prettify(formatter='html')
        # print(self._pretty_soup)
        items = self._soup.find_all('item')
        for item in items:
            split_item = re.split('<.*?>', item.text)
            self._append_info('구', land_name)
            self._append_info('거래금액', split_item[1].replace(',', ''))
            self._append_info('건축년도', split_item[2])
            self._append_info('년', split_item[3])
            self._append_info('법정동', split_item[4])
            self._append_info('단지명', split_item[5])
            self._append_info('월', split_item[6])
            self._append_info('일', split_item[7])
            self._append_info('전용면적', split_item[8])
            self._append_info('지번', split_item[9])
            self._append_info('층', split_item[11])

    def _query(self, land_name, deal_ymd):
        land_code = self._bjd_code_df[land_name]
        self._land_code = land_code
        self._deal_ymd = deal_ymd
        self._create_url()
        self._request()
        self._parse_xml(land_name)

    def _get_ymd(self, start_year, start_month, end_year, end_month):
        deal_ymds = []
        for year in range(start_year, end_year+1):
            month0 = 1
            month1 = 12
            if year == start_year:
                month0 = start_month
            if year == end_year:
                month1 = end_month
            for month in range(month0, month1+1):
                ymd = str(year) + str(month).zfill(2)
                deal_ymds.append(ymd)
        return deal_ymds

    def get(self, gu_names, start_year, start_month, end_year, end_month):
        deal_ymds = self._get_ymd(start_year, start_month, end_year, end_month)
        for gu_name in gu_names:
            for deal_ymd in deal_ymds:
                print(gu_name, deal_ymd)
                self._query(gu_name, deal_ymd)

        self.items = pd.DataFrame(self.infos)

    def to_excel(self, xlsx_name, sheet_name='sheet1'):
        self.items.to_excel(xlsx_name, sheet_name=sheet_name)
