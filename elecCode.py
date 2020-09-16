from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd


class ElecCode:
    def __init__(self, key):
        self.items = []
        self.elec_codes = []
        self._callback_url = 'http://apis.data.go.kr/9760000/CommonCodeService/getCommonSgCodeList'
        self._service_key = key
        self.sgid = []
        self.sgtypecode = []
        self.sgname = []
        self.sgvotedate = []
        self.num = []

    def _create_url(self):
        query_params = '?' + urlencode(
            {quote_plus('ServiceKey'): self._service_key, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '100'})
        self._url = self._callback_url + query_params

    def _request(self):
        request = Request(self._url)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        self._soup = BeautifulSoup(response_body, 'html.parser')

    def _parse_xml(self):
        self._pretty_soup = self._soup.prettify()
        print(self._pretty_soup)
        items = self._soup.find_all('item')
        for item in items:
            self.sgid.append(item.find('sgid').string)
            self.sgtypecode.append(item.find('sgtypecode').string)
            self.sgname.append(item.find('sgname').string)
            self.sgvotedate.append(item.find('sgvotedate').string)
            self.num.append(item.find('num').string)

    def _query(self):
        self._create_url()
        self._request()
        self._parse_xml()

    def get(self):
        self._query()
        self.items = pd.DataFrame({'선거ID': self.sgid,
                                   '선거종류코드': self.sgtypecode,
                                   '선거명': self.sgname,
                                   '선거일자': self.sgvotedate,
                                   '결과순서': self.num})
