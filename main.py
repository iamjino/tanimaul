# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import aptList as al
import aptInfo as ai
import aptPrice as ap
import elecPlace as ep
import aptPriceAnalysis as apa
import elecZone as ez
import elecResult as er
import aptInfoMerge as am
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
#          'doc_kapt_list': 'doc/KAPT 공동주택 현황.xlsx',
#          'conf_kapt_list_fix': 'conf/KAPT 공동주택 현황-수정.xlsx',
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

doc_kapt_list = 'doc/KAPT 공동주택 현황.xlsx'
conf_kapt_list_fix = 'conf/KAPT 공동주택 현황-수정.xlsx'

doc_apt_list = 'doc/공동주택 현황.xlsx'
doc_elec_place_list = 'doc/투표구 관할구역.xlsx'
doc_elec_zone_list = 'doc/투표소별 단지 현황.xlsx'
doc_apt_price = 'doc/아파트 매매 실거래가.xlsx'

price_chart = 'chart.png'
start_year = 2007
start_month = 1
end_year = 2020
end_month = 12

if False:
    # Get Apt List
    aptList = al.AptList(service_key)

    # target_gus = []
    target_gus = ['기흥구', '수지구', '처인구']
    target_dongs = ['동백동']
    # target_dongs = ['동백동', '중동', '마북동', '보정동']
    aptList.get(conf_bjd_code, target_gus, target_dongs)
    print(aptList.items)

    apt_codes = aptList.items['단지코드']
    # apt_codes = ['A44691615', 'A44679103']
    print(apt_codes)

    # Get Apt Info
    aptInfo = ai.AptInfo(service_key)
    print(aptInfo.items)
    aptInfo.get(apt_codes)

    # apt_infos = pd.concat(aptList.items, aptInfo.items, axis=1)
    apt_infos = pd.merge(aptList.items, aptInfo.items, on='단지코드')
    # apt_infos['단지명 일치'] = apt_infos['단지명'] == apt_infos['단지명2']
    apt_infos.to_excel(doc_kapt_list)
    print(apt_infos)

if False:
    apt_info_merge = am.AptInfoMerge(conf_yiapt_list_file, conf_yiapt_list_sheet, doc_kapt_list, conf_kapt_list_fix)
    apt_info_merge.run()
    apt_info_merge.to_excel(doc_apt_list)

if False:
    # elec_list = el.ElecCode(service_key)
    # elec_list.get()
    # print(elec_list.items)
    # elec_list.items.to_excel('elecCode_sg.xlsx', sheet_name='sg')
    elec_place = ep.ElecPlace(conf_yi_elecplace_file, conf_yi_elecplace_sheet)
    elec_place.decode()
    elec_place.to_excel(doc_elec_place_list)

if False:
    elec_zone = ez.elecZone(conf_yiaddr_file, conf_yiaddr_sheet, conf_yiaddr_file_fix, doc_apt_list, doc_elec_place_list)
    elec_zone.match_zone()
    elec_zone.to_excel(doc_elec_zone_list)

if False:
    apt_price = ap.AptPrice(service_key)
    target_gus = ['기흥구']
    apt_price.get(target_gus, start_year, start_month, end_year, end_month)
    apt_price.to_excel(doc_apt_price)

if True:
    apt_price_analysis = apa.AptPriceAnalysis(doc_apt_price, price_chart, start_year, start_month, end_year, end_month)
    apt_price_analysis.analysis('중동 870')

if False:
    elec_result = er.ElecResult()
    elec_result.run()
