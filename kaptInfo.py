from urllib.parse import urlencode, quote_plus
import pandas as pd
from govData import GovData


class KaptInfo(GovData):
    def __init__(self, key):
        url = 'http://apis.data.go.kr/1611000/AptBasisInfoService/getAphusBassInfo'
        super(self.__class__, self).__init__(url, key)

        self._kapt_code = ''
        self.data = {
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

    def _set_query_param(self):
        self._query_param = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('kaptCode'): self._kapt_code})

    def _parse_xml(self):
        self._parse_xml_line(self._soup, '단지코드', 'kaptcode')
        self._parse_xml_line(self._soup, '단지명', 'kaptname')
        self._parse_xml_line(self._soup, '단지분류', 'codeaptnm')
        self._parse_xml_line(self._soup, '도로명주소', 'dorojuso')
        self._parse_xml_line(self._soup, '분양형태', 'codesalenm')
        self._parse_xml_line(self._soup, '난방방식', 'codeheatnm')
        self._parse_xml_line(self._soup, '복도유형', 'codehallnm')
        self._parse_xml_line(self._soup, '사용승인일', 'kaptusedate')
        self._parse_xml_line(self._soup, '동수', 'kaptdongcnt')
        self._parse_xml_line(self._soup, '세대수', 'kaptdacnt')
        self._parse_xml_line(self._soup, '호수', 'hocnt')
        self._parse_xml_line(self._soup, '전용면적 60이하', 'kaptmparea_60')
        self._parse_xml_line(self._soup, '전용면적 60-85이하', 'kaptmparea_85')
        self._parse_xml_line(self._soup, '전용면적 85-135이하', 'kaptmparea_135')
        self._parse_xml_line(self._soup, '전용면적 135초과', 'kaptmparea_136')
        self._parse_xml_line(self._soup, '관리방식', 'codemgrnm')
        self._parse_xml_line(self._soup, '관리사무소 연락처', 'kapttel')
        self._parse_xml_line(self._soup, '관리사무소 팩스', 'kaptfax')
        self._parse_xml_line(self._soup, '시행사', 'kaptacompany')
        self._parse_xml_line(self._soup, '시공사', 'kaptbcompany')
        self._parse_xml_line(self._soup, '홈페이지 주소', 'kapturl')
        self._parse_xml_line(self._soup, '건축물대장상 연면적', 'kapttarea')
        self._parse_xml_line(self._soup, '관리비부과면적', 'kaptmarea')
        self._parse_xml_line(self._soup, '단지 전용면적합', 'privarea')

    def _get_bjd_addr(self):
        kaptname = self._soup.find('kaptname').string
        kaptaddr = self._soup.find('kaptaddr').string
        kaptaddr = kaptaddr.replace('경기도 용인', '경기도 용인시 ')
        kaptaddr = kaptaddr.replace(kaptname, '').strip()
        self.data['법정동주소'].append(kaptaddr)

    def get(self, kapt_codes):
        for kapt_code in kapt_codes:
            self._kapt_code = kapt_code
            self._query()
            self._get_bjd_addr()
        self.items = pd.DataFrame(self.data)
