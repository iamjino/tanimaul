from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd


class AptInfo:
    def __init__(self, key):
        self.items = []
        self._callback_url = 'http://apis.data.go.kr/1611000/AptBasisInfoService/getAphusBassInfo'
        self._service_key = key
        self.codeaptnm = []
        self.codehallnm = []
        self.codeheatnm = []
        self.codemgrnm = []
        self.codesalenm = []
        self.dorojuso = []
        self.hocnt = []
        self.kaptacompany = []
        self.kaptaddr = []
        self.kaptbcompany = []
        self.kaptcode = []
        self.kaptdongcnt = []
        self.kaptmarea = []
        self.kaptmparea_135 = []
        self.kaptmparea_136 = []
        self.kaptmparea_60 = []
        self.kaptmparea_85 = []
        self.kaptname = []
        self.kapttarea = []
        self.kapttel = []
        self.kaptfax = []
        self.kapturl = []
        self.kaptusedate = []
        self.kaptdacnt = []
        self.privarea = []

    def _create_url(self):
        query_params = '?' + urlencode(
            {quote_plus('serviceKey'): self._service_key, quote_plus('kaptCode'): self._kapt_code})
        self._url = self._callback_url + query_params

    def _request(self):
        request = Request(self._url)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        self._soup = BeautifulSoup(response_body, 'html.parser')

    def _parse_xml(self):
        # self._pretty_soup = self._soup.prettify()
        # print(self._pretty_soup)
        self.codeaptnm.append(self._soup.find('codeaptnm').string)
        self.codehallnm.append(self._soup.find('codehallnm').string)
        self.codeheatnm.append(self._soup.find('codeheatnm').string)
        self.codemgrnm.append(self._soup.find('codemgrnm').string)
        self.codesalenm.append(self._soup.find('codesalenm').string)
        self.dorojuso.append(self._soup.find('dorojuso').string)
        self.hocnt.append(self._soup.find('hocnt').string)
        self.kaptacompany.append(self._soup.find('kaptacompany').string)
        self.kaptaddr.append(self._soup.find('kaptaddr').string)
        self.kaptbcompany.append(self._soup.find('kaptbcompany').string)
        self.kaptcode.append(self._soup.find('kaptcode').string)
        self.kaptdongcnt.append(self._soup.find('kaptdongcnt').string)
        self.kaptmarea.append(self._soup.find('kaptmarea').string)
        self.kaptmparea_135.append(self._soup.find('kaptmparea_135').string)
        self.kaptmparea_136.append(self._soup.find('kaptmparea_136').string)
        self.kaptmparea_60.append(self._soup.find('kaptmparea_60').string)
        self.kaptmparea_85.append(self._soup.find('kaptmparea_85').string)
        self.kaptname.append(self._soup.find('kaptname').string)
        self.kapttarea.append(self._soup.find('kapttarea').string)
        self.kapttel.append(self._soup.find('kapttel').string)
        self.kaptfax.append(self._soup.find('kaptfax').string)
        self.kapturl.append(self._soup.find('kapturl').string)
        self.kaptusedate.append(self._soup.find('kaptusedate').string)
        self.kaptdacnt.append(self._soup.find('kaptdacnt').string)
        self.privarea.append(self._soup.find('privarea').string)

    def _query(self):
        self._create_url()
        self._request()
        self._parse_xml()

    def get(self, kapt_code_df):
        for kapt_code in kapt_code_df:
            self._kapt_code = kapt_code
            self._query()
        self.items = pd.DataFrame({'단지코드': self.kaptcode,
                                   '단지명2': self.kaptname,
                                   '단지분류': self.codeaptnm,
                                   '법정동주소': self.kaptaddr,
                                   '도로명주소': self.dorojuso,
                                   '분양형태': self.codesalenm,
                                   '난방방식': self.codeheatnm,
                                   '복도유형': self.codehallnm,
                                   '사용승인일': self.kaptusedate,
                                   '동수': self.kaptdongcnt,
                                   '세대수': self.kaptdacnt,
                                   '호수': self.hocnt,
                                   '전용면적 60이하': self.kaptmparea_60,
                                   '전용면적 60-85이하': self.kaptmparea_85,
                                   '전용면적 85-135이하': self.kaptmparea_135,
                                   '전용면적 135초과': self.kaptmparea_136,
                                   '관리방식': self.codemgrnm,
                                   '관리사무소 연락처': self.kapttel,
                                   '관리사무소 팩스': self.kaptfax,
                                   '시행사': self.kaptacompany,
                                   '시공사': self.kaptbcompany,
                                   '홈페이지 주소': self.kapturl,
                                   '건축물대장상 연면적': self.kapttarea,
                                   '관리비부과면적': self.kaptmarea,
                                   '단지 전용면적합': self.privarea})
