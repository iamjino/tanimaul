from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd


class AptInfo:
    def __init__(self, key):
        self._callback_url = 'http://apis.data.go.kr/1611000/AptBasisInfoService/getAphusBassInfo'
        self._service_key = key
        self._kapt_code = ''
        self.items = []
        self.infos = {
            '단지코드': [],
            '단지명': [],
            '단지분류': [],
            '법정동주소': [],
            '도로명주소': [],
            '분양형태': [],
            '난방방식': [],
            '복도유형': [],
            '사용승인일': [],
            '동수': [],
            '세대수': [],
            '호수': [],
            '전용면적 60이하': [],
            '전용면적 60-85이하': [],
            '전용면적 85-135이하': [],
            '전용면적 135초과': [],
            '관리방식': [],
            '관리사무소 연락처': [],
            '관리사무소 팩스': [],
            '시행사': [],
            '시공사': [],
            '홈페이지 주소': [],
            '건축물대장상 연면적': [],
            '관리비부과면적': [],
            '단지 전용면적합': []
        }

    def _create_url(self):
        query_params = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('kaptCode'): self._kapt_code})
        self._url = self._callback_url + query_params

    def _request(self):
        request = Request(self._url)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        self._soup = BeautifulSoup(response_body, 'html.parser')

    def _append_info(self, key, code):
        value = self._soup.find(code)
        if isinstance(value, type(None)):
            value = ''
        else:
            value = value.string.strip()
        self.infos[key].append(value)

    def _parse_xml(self):
        self._pretty_soup = self._soup.prettify()
        # print(self._pretty_soup)
        self._append_info('단지코드', 'kaptcode')
        self._append_info('단지명', 'kaptname')
        self._append_info('단지분류', 'codeaptnm')
        # self._append_info('법정동주소', 'kaptaddr')
        self._append_info('도로명주소', 'dorojuso')
        self._append_info('분양형태', 'codesalenm')
        self._append_info('난방방식', 'codeheatnm')
        self._append_info('복도유형', 'codehallnm')
        self._append_info('사용승인일', 'kaptusedate')
        self._append_info('동수', 'kaptdongcnt')
        self._append_info('세대수', 'kaptdacnt')
        self._append_info('호수', 'hocnt')
        self._append_info('전용면적 60이하', 'kaptmparea_60')
        self._append_info('전용면적 60-85이하', 'kaptmparea_85')
        self._append_info('전용면적 85-135이하', 'kaptmparea_135')
        self._append_info('전용면적 135초과', 'kaptmparea_136')
        self._append_info('관리방식', 'codemgrnm')
        self._append_info('관리사무소 연락처', 'kapttel')
        self._append_info('관리사무소 팩스', 'kaptfax')
        self._append_info('시행사', 'kaptacompany')
        self._append_info('시공사', 'kaptbcompany')
        self._append_info('홈페이지 주소', 'kapturl')
        self._append_info('건축물대장상 연면적', 'kapttarea')
        self._append_info('관리비부과면적', 'kaptmarea')
        self._append_info('단지 전용면적합', 'privarea')

    def _get_bjd_addr(self):
        kaptname = self._soup.find('kaptname').string
        kaptaddr = self._soup.find('kaptaddr').string
        kaptaddr = kaptaddr.replace('경기도 용인', '경기도 용인시 ')
        kaptaddr = kaptaddr.replace(kaptname, '').strip()
        self.infos['법정동주소'].append(kaptaddr)

    def _query(self):
        self._create_url()
        self._request()
        self._parse_xml()
        self._get_bjd_addr()

    def get(self, kapt_code_df):
        for kapt_code in kapt_code_df:
            self._kapt_code = kapt_code
            self._query()
        self.items = pd.DataFrame(self.infos)
