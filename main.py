# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import kaptList as al
import kaptInfo as ai
import houseDeal as hd
import housePriceAnalysis as hpa
import elecResult as er
import houseInfo as hi
import rentChangeRate as cr
import elecCode as el
import pandas as pd
import openpyxl
import requests
import necPollAddress as npa
import necPollHouse as nph
import necResult as nr
import necPollbook as np
import necAnalysis as na
import math


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

if False:
    elec_list = el.ElecCode(service_key)
    # elec_list.get()
    # print(elec_list.items)
    # elec_list.items.to_excel('elecCode_sg.xlsx', sheet_name='sg')

if False:
    elec_result = er.ElecResult()
    elec_result.run()

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

conf_yi_elecplace_file_2017 = 'conf/투표구 관할구역-19대 대선-용인시기흥구.xlsx'
conf_yi_elecplace_file_2016 = 'conf/투표구 관할구역-20대 총선-용인시기흥구.xlsx'
conf_yi_elecplace_file_2020 = 'conf/투표구 관할구역-21대 총선-용인시기흥구.xlsx'

conf_yiaddr_file = 'conf/용인시 통리반 관할구역.xlsx'
conf_yiaddr_sheet = 'step1'
conf_yiaddr_file_fix = 'conf/용인시 통리반 관할구역-수정.xlsx'

doc_kapt_info = 'doc/KAPT 공동주택 현황.xlsx'
conf_kapt_info_fix = 'conf/KAPT 공동주택 현황-수정.xlsx'

doc_house_info = 'doc/공동주택 현황.xlsx'
conf_house_info = 'conf/공동주택 현황-보완.xlsx'
doc_poll_addr_list = 'doc/투표구 관할주소.xlsx'
doc_poll_house_list = 'doc/투표구 관할단지.xlsx'
doc_trade_price = 'doc/주택 매매 현황.xlsx'
doc_rent_price = 'doc/주택 임대차 현황.xlsx'
doc_poll_house_info = 'doc/투표구 관할단지 정보.xlsx'

start_year = 2006
start_month = 1
end_year = 2020
end_month = 12

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
    house_info.fill_data(conf_house_info)
    house_info.print()
    house_info.to_excel(doc_house_info)

if False:
    rt_urls = {'apt_trade': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade',
               'apt_rent': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent',
               'rh_trade': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade',
               'rh_rent': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent'}
    target_gus = ['기흥구', '수지']

    def get_deal_list(deal_type, house_types):
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
        return house_prices

    def postprocess_rent_prices(my_rent_prices):
        conf_rent_change_rate = 'conf/전월세 전환율.xlsx'
        rent_change_rates = cr.RentChageRate(conf_rent_change_rate)
        my_rent_prices['전월세 전환율'] = ''
        my_rent_prices['거래금액'] = ''

        for index in range(my_rent_prices.index.size):
            rent = int(my_rent_prices.at[index, '월세금액'])
            deposit = int(my_rent_prices.at[index, '보증금액'])
            gu_name = my_rent_prices.at[index, '구']
            year = int(my_rent_prices.at[index, '년'])
            month = int(my_rent_prices.at[index, '월'])

            rate = rent_change_rates.get(gu_name, year, month)

            price = (rent*12) / rate * 100 + deposit
            price = round(price, -2)
            my_rent_prices.at[index, '전월세 전환율'] = rate
            my_rent_prices.at[index, '거래금액'] = price

        return my_rent_prices

    trade_prices = get_deal_list('trade', ['apt', 'rh'])
    trade_prices.to_excel(doc_trade_price)

    rent_prices = get_deal_list('rent', ['apt', 'rh'])
    rent_prices = postprocess_rent_prices(rent_prices)
    rent_prices.to_excel(doc_rent_price)

if False:
    poll_addr_2016 = npa.NecPollAddress('20', '국회의원선거', conf_yi_elecplace_file_2016)
    poll_addr_2017 = npa.NecPollAddress('19', '대통령선거', conf_yi_elecplace_file_2017)
    poll_addr_2020 = npa.NecPollAddress('21', '국회의원선거', conf_yi_elecplace_file_2020)
    poll_addr = pd.concat([poll_addr_2016.items, poll_addr_2017.items, poll_addr_2020.items])
    poll_addr.to_excel(doc_poll_addr_list)

if False:
    poll_house = nph.NecPollHouse(conf_yiaddr_file, conf_yiaddr_sheet, conf_yiaddr_file_fix, doc_house_info, doc_poll_addr_list)
    poll_house.run()
    poll_house.to_excel(doc_poll_house_list)

if False:
    # 투표구 관할단지 정보 생성
    df_house_info_full = pd.read_excel(doc_house_info)
    df_house_info_full.drop(['법정동', '단지명'], axis=1, inplace=True)
    df_house_info_poll = pd.read_excel(doc_poll_house_list)
    df_house_info_poll['간략 법정동주소'] = ''

    for index, row in df_house_info_poll.iterrows():
        value = row['법정동']
        if value in ['죽전1동', '상현2동']:
            df_house_info_poll.at[index, '간략 법정동주소'] = '수지구 ' + row['주소']
        else:
            df_house_info_poll.at[index, '간략 법정동주소'] = '기흥구 ' + row['주소']
    df_house_infos = pd.merge(df_house_info_poll, df_house_info_full, on='간략 법정동주소')
    df_house_infos.to_excel(doc_poll_house_info)

if False:
    # 주택 매매 차트 생성: 투표구 관할단지 정보 생성 활성화 필요
    house_price_analysis = hpa.HousePriceAnalysis(doc_trade_price, start_year, start_month, end_year, end_month)
    file_path = 'doc/img/'
    for index, row in df_house_infos.iterrows():
        if not (row['분양형태'] == '국민임대' or row['분양형태'] == '임대'):
            addr = row['주소']
            if addr == '보정동 878-22':
                addr = '보정동 878-18'
            elif addr == '보정동 909-5':
                addr = '보정동 909'

            addr_full = row['간략 법정동주소'] + ' ' + row['단지명']
            chart_title = addr_full + ' 매매'
            print(file_path + chart_title)
            house_price_analysis.analysis(addr, file_path, chart_title)

if False:
    # 주택 임대차 차트 생성: 투표구 관할단지 정보 생성 활성화 필요
    house_price_analysis = hpa.HousePriceAnalysis(doc_rent_price, start_year, start_month, end_year, end_month)
    file_path = 'doc/img/'
    for index, row in df_house_infos.iterrows():
        addr = row['주소']
        if addr == '보정동 878-22':
            addr = '보정동 878-18'
        elif addr == '보정동 909-5':
            addr = '보정동 909'

        addr_full = row['간략 법정동주소'] + ' ' + row['단지명']
        chart_title = addr_full + ' 임대차'
        print(file_path + chart_title)
        house_price_analysis.analysis(addr, file_path, chart_title)

if False:
    # 선거인명부 개표결과 분석
    # nr_file_in = '선거통계/개표현황(투표구별)-21대 총선 용인시정.xlsx'
    # nr_file_out = 'nec_assembly21.xlsx'
    # nec_result = nr.NecResult('assembly21')
    # nec_result.open(nr_file_in, nr_file_out)
    #
    # nr_file_in = '선거통계/개표현황(투표구별)-20대 총선 용인시정.xlsx'
    # nr_file_out = 'nec_assembly20.xlsx'
    # nec_result = nr.NecResult('assembly20')
    # nec_result.open(nr_file_in, nr_file_out)

    nr_file_in = '선거통계/개표현황(투표구별)-19대 대선 기흥구.xlsx'
    nr_file_out = 'nec_president19.xlsx'
    nec_result = nr.NecResult('president19')
    nec_result.open(nr_file_in, nr_file_out)
    #
    # np_file_in = '선거통계/선거인수현황-21대 총선 기흥구.xlsx'
    # np_file_out = 'nec_pollbook_assembly21.xlsx'
    # nec_pollbook = np.NecPollbook()
    # nec_pollbook.open(np_file_in, np_file_out)

    # np_file_in = '선거통계/선거인수현황-20대 총선 기흥구.xlsx'
    # np_file_out = 'nec_pollbook_assembly20.xlsx'
    # nec_pollbook = np.NecPollbook()
    # nec_pollbook.open(np_file_in, np_file_out)

    np_file_in = '선거통계/선거인수현황-19대 대선 기흥구.xlsx'
    np_file_out = 'nec_pollbook_president19.xlsx'
    nec_pollbook = np.NecPollbook()
    nec_pollbook.open(np_file_in, np_file_out)

if True:
    nec_analysis = na.NecAnalysis(nec_result, nec_pollbook)
    nec_analysis.run(doc_poll_house_info)
