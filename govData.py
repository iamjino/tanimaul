from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from abc import *


class GovData(metaclass=ABCMeta):
    def __init__(self, url, key):
        self._callback_url = url
        self._service_key = key
        self._query_param = ''
        self.items = ''
        self.data = {}

    def _set_url(self):
        self._url = self._callback_url + self._query_param

    def _request(self):
        request = Request(self._url)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        self._soup = BeautifulSoup(response_body, 'html.parser')

    def _append_data(self, key, value):
        if isinstance(value, type(None)):
            value = ''
        elif str(type(value)) == "<class 'bs4.element.Tag'>":
            value = value.string.strip()
        else:
            value = value.strip()
        self.data[key].append(value)

    def _parse_xml_line(self, item, key, code):
        value = item.find(code)
        self._append_data(key, value)

    @abstractmethod
    def _set_query_param(self):
        pass

    @abstractmethod
    def _parse_xml(self):
        pass

    def _query(self):
        self._set_query_param()
        self._set_url()
        self._request()
        self._parse_xml()

    def print_xml(self):
        print(self._soup.prettify(formatter='html'))

    def to_excel(self, xlsx_name, sheet_name='sheet1'):
        self.items.to_excel(xlsx_name, sheet_name=sheet_name)
