# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import kaptList as al
import kaptInfo as ai
import houseDeal as hd
import elecPlace as ep
import aptPriceAnalysis as apa
import elecZone as ez
import elecResult as er
import houseInfo as hi
import elecCode as el
import pandas as pd
import openpyxl
import requests


def print_hi(name1):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi,', name1)  # Press ⌘F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Tanimaul')

if False:
    from bs4 import BeautifulSoup
    import urllib.request as req

    url = 'https://ko.wikisource.org/wiki/%EC%A0%80%EC%9E%90:%ED%95%9C%EC%9A%A9%EC%9A%B4'
    # url = '#mw-content-text > div.mw-parser-output > ul:nth-child(7) > li:nth-child(1) > a'
    res = req.urlopen(url)

    soup = BeautifulSoup(res, 'html.parser')
    list = soup.select("#mw-content-text > div.mw-parser-output > ul > li > a")
    for a in list:
        name = a.string
        print(name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
service_key = 'wRaEeY%2BpbPZX3OjIYLLt74uO5%2BAY7DXQJ9MWyyGodai94K7JvfjtLL%2FTRzkFuMxfb6SmuGqcM2YSCcVa4V1KeQ%3D%3D'
service_key = requests.utils.unquote(service_key)

# files = {'conf_bjd_code': './conf/용인시 법정동 코드.txt',
#          'conf_yiapt_list_file': 'conf/용인시 공동주택 현황.xlsx',
#          'conf_yiapt_list_sheet': 'summary',
#          'doc_kapt_info': 'doc/KAPT 공동주택 현황.xlsx',
#          'conf_kapt_info_fix': 'conf/KAPT 공동주택 현황-수정.xlsx',
#          'doc_apt_list': 'doc/공동주택 현황.xlsx'
#          }

conf_bjd_code = './conf/용인시 법정동 코드.txt'

conf_yiapt_list_file = 'conf/용인시 공동주택 현황.xlsx'
conf_yiapt_list_sheet = 'summary'

conf_yi_elecplace_file = 'conf/용인시 투표구 관할구역.xlsx'
conf_yi_elecplace_sheet = '2020년 제21대 국회의원선거'

conf_yiaddr_file = 'conf/용인시 통리반 관할구역.xlsx'
conf_yiaddr_sheet = 'step1'
conf_yiaddr_file_fix = 'conf/용인시 통리반 관할구역-수정.xlsx'

doc_kapt_info = 'doc/KAPT 공동주택 현황.xlsx'
conf_kapt_info_fix = 'conf/KAPT 공동주택 현황-수정.xlsx'

doc_house_info = 'doc/공동주택 현황.xlsx'
doc_elec_place_list = 'doc/투표구 관할구역.xlsx'
doc_elec_zone_list = 'doc/투표소별 단지 현황.xlsx'
doc_trade_price = 'doc/주택 매매 현황.xlsx'
doc_rent_price = 'doc/주택 전월세 현황.xlsx'

price_chart = 'chart.png'
start_year = 2019
start_month = 12
end_year = 2020
end_month = 1

if False:
    def get_bjd_code(conf_bjd_code):
        bjd_code_df = pd.read_csv(conf_bjd_code, sep='\t', encoding='EUC-KR')
        bjd_code_df.columns = ['bjd_code', 'dong_name', 'valid']
        bjd_code_df.columns.name = 'Code Info'
        return bjd_code_df.loc[bjd_code_df['valid'] == '존재', :]

    # Get Apt List
    bjd_codes = get_bjd_code(conf_bjd_code)
    target_gus = ['기흥구', '수지구', '처인구']
    # target_gus = []
    target_dongs = ['동백동']

    kapt_list = al.KaptList(service_key)
    kapt_list.get(bjd_codes, target_gus, target_dongs)

    # Get Apt Info
    apt_codes = kapt_list.items['단지코드']

    kapt_info = ai.KaptInfo(service_key)
    kapt_info.get(apt_codes)

    kapt_info_final = pd.merge(kapt_list.items, kapt_info.items, on='단지코드')
    kapt_info_final.to_excel(doc_kapt_info)
    print(kapt_info_final)

if True:
    house_info = hi.HouseInfo(conf_yiapt_list_file, conf_yiapt_list_sheet, doc_kapt_info, conf_kapt_info_fix)
    house_info.run()
    house_info.print()
    house_info.to_excel(doc_house_info)

if False:
    # elec_list = el.ElecCode(service_key)
    # elec_list.get()
    # print(elec_list.items)
    # elec_list.items.to_excel('elecCode_sg.xlsx', sheet_name='sg')
    elec_place = ep.ElecPlace(conf_yi_elecplace_file, conf_yi_elecplace_sheet)
    elec_place.decode()
    elec_place.to_excel(doc_elec_place_list)

if False:
    elec_zone = ez.elecZone(conf_yiaddr_file, conf_yiaddr_sheet, conf_yiaddr_file_fix, doc_house_info, doc_elec_place_list)
    elec_zone.match_zone()
    elec_zone.to_excel(doc_elec_zone_list)

if False:
    rt_urls = {'apt_trade': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade',
               'apt_rent': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent',
               'rh_trade': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade',
               'rh_rent': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent'}
    target_gus = ['기흥구']

    def get_deal_list(deal_type, export_filename, house_types):
        deal_items = []
        for house_type in house_types:
            key = house_type + '_' + deal_type
            print(key, rt_urls[key])
            deal = ''
            if deal_type == 'trade':
                deal = hd.HouseDealTrade(rt_urls[key], service_key)
            elif deal_type == 'rent':
                deal = hd.HouseDealRent(rt_urls[key], service_key)
            deal.get(target_gus, start_year, start_month, end_year, end_month)
            deal_items.append(deal.items)

        house_prices = pd.concat(deal_items, ignore_index=True)
        house_prices.to_excel(export_filename)

    get_deal_list('rent', doc_rent_price, ['apt', 'rh'])
    get_deal_list('trade', doc_trade_price, ['apt', 'rh'])

if False:
    apt_price_analysis = apa.AptPriceAnalysis(doc_rent_price, price_chart, start_year, start_month, end_year, end_month)
    apt_price_analysis.analysis('중동 870')

if False:
    elec_result = er.ElecResult()
    elec_result.run()
