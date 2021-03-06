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
import necZoneAddress as nza
import necZoneHouse as nzh
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
#          'conf_apt_list': 'conf/용인시 공동주택 현황.xlsx',
#          'conf_yiapt_list_sheet': 'summary',
#          'doc_kapt_info': 'doc/KAPT 공동주택 현황.xlsx',
#          'conf_kapt_info_fix': 'conf/KAPT 공동주택 현황-수정.xlsx',
#          'doc_apt_list': 'doc/공동주택 현황.xlsx'
#          }

conf_bjd_code = './conf/용인시 법정동 코드.txt'

conf_kapt_info_fix = 'conf/KAPT 공동주택 현황-수정.xlsx'
doc_kapt_info = 'doc/KAPT 공동주택 현황.xlsx'

conf_apt_list = 'conf/용인시 공동주택 현황.xlsx'
conf_apt_list_sheet = 'summary'


conf_house_info_fix = 'conf/공동주택 현황-수정.xlsx'
doc_house_info = 'doc/공동주택 현황.xlsx'

conf_rent_rate = 'conf/전월세 전환율.xlsx'
doc_trade_price = 'doc/주택 매매 현황.xlsx'
doc_rent_price = 'doc/주택 임대차 현황.xlsx'

doc_house_info_zone = 'doc/공동주택 현황(투표구 포함).xlsx'


sg_ids = ['20대 총선', '19대 대선', '21대 총선']

start_year = 2006
start_month = 1
end_year = 2020
end_month = 12

if False:
    def get_bjd_code(code_file):
        bjd_code_df = pd.read_csv(code_file, sep='\t', encoding='EUC-KR')
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
    kapt_info_final.to_excel(doc_kapt_info, index=False)
    print(kapt_info_final)

if False:
    house_info = hi.HouseInfo(conf_apt_list, conf_apt_list_sheet, doc_kapt_info, conf_kapt_info_fix)

    house_info.run()
    house_info.fill_data(conf_house_info_fix)
    house_info.print()
    house_info.items.to_excel(doc_house_info, index=False)

if False:
    rt_urls = {'apt_trade': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade',
               'apt_rent': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent',
               'rh_trade': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade',
               'rh_rent': 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent'}
    target_gus = ['기흥구', '수지구']

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
        rent_change_rates = cr.RentChageRate(conf_rent_rate)
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
    # 주택 매매 차트 생성: 투표구 공동주택 정보 필요(df_house_infos)
    df_house_infos = pd.read_excel(doc_house_info)
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
    # 주택 임대차 차트 생성: 투표구 공동주택 정보 필요
    df_house_infos = pd.read_excel(doc_house_info)
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

# Reruned until here

if True:
# conf_zone_addr = {"20대 총선": ['conf/투표구 관할구역-20대 총선 기흥구.xlsx', 'conf/투표구 관할구역-20대 총선 수지구.xlsx'],
#                   "19대 대선": ['conf/투표구 관할구역-19대 대선 기흥구.xlsx', 'conf/투표구 관할구역-19대 대선 수지구.xlsx'],
#                   "21대 총선": ['conf/투표구 관할구역-21대 총선 기흥구.xlsx']}
    conf_zone_addr = {"20대 총선": ['conf/투표구 관할구역-20대 총선 기흥구.xlsx'],
                      "19대 대선": ['conf/투표구 관할구역-19대 대선 기흥구.xlsx'],
                      "21대 총선": ['conf/투표구 관할구역-21대 총선 기흥구.xlsx']}
    doc_zone_addr = {}

    def iter_nza(sg_id, file_ins):
        file_out = 'doc/투표구 관할통-' + sg_id + '.xlsx'
        dfs = []
        for file_in in file_ins[sg_id]:
            zone_addr = nza.NecZoneAddress(sg_id, file_in)
            dfs.append(zone_addr.items)
        zone_addrs = pd.concat(dfs)
        zone_addrs.to_excel(file_out, index=False)
        return file_out
    for sg_id in sg_ids:
        doc_zone_addr[sg_id] = iter_nza(sg_id, conf_zone_addr)

if True:
    doc_zone_addr = {"20대 총선": 'doc/투표구 관할통-20대 총선.xlsx',
                     "19대 대선": 'doc/투표구 관할통-19대 대선.xlsx',
                     "21대 총선": 'doc/투표구 관할통-21대 총선.xlsx'}
    conf_law_addr = {"20대 총선": 'conf/용인시 통리반 설치 조례-20대 총선.xlsx',
                     "19대 대선": 'conf/용인시 통리반 설치 조례-19대 대선.xlsx',
                     "21대 총선": 'conf/용인시 통리반 설치 조례-21대 총선.xlsx'}
    conf_law_addr_sheet = 'analysis'
    conf_law_addr_fix = 'conf/용인시 통리반 설치 조례-수정.xlsx'

    doc_zone_house = {}
    doc_zone_house_raw = {}
    for sg_id in sg_ids:
        zone_house = nzh.NecZoneHouse(conf_law_addr[sg_id], conf_law_addr_sheet, conf_law_addr_fix, doc_house_info, doc_zone_addr[sg_id])
        zone_house.run()
        file_out = 'doc/투표구 관할단지-' + sg_id + '.xlsx'
        zone_house.items.to_excel(file_out, index=False)
        doc_zone_house[sg_id] = file_out
        raw_file_out = 'doc/투표구 관할단지(상세)-' + sg_id + '.xlsx'
        zone_house.law_addr.to_excel(raw_file_out, index=False)
        doc_zone_house_raw[sg_id] = raw_file_out

if False:
    doc_zone_house = {"20대 총선": 'doc/투표구 관할단지-20대 총선.xlsx',
                      "19대 대선": 'doc/투표구 관할단지-19대 대선.xlsx',
                      "21대 총선": 'doc/투표구 관할단지-21대 총선.xlsx'}
if True:
    # 공동주택 현황에 투표구 정보 추가
    df_house_infos = pd.read_excel(doc_house_info)
    for sg_id in sg_ids:
        df_zone_house = pd.read_excel(doc_zone_house[sg_id])
        df_zone_house['간략 법정동주소'] = ''
        df_zone_house.rename(columns={'투표구명': sg_id}, inplace=True)

        for index, row in df_zone_house.iterrows():
            df_zone_house.at[index, '간략 법정동주소'] = row['구'] + ' ' + row['주소']

        df_zone_house_subset = df_zone_house[[sg_id, '간략 법정동주소']]
        df_house_infos = pd.merge(df_house_infos, df_zone_house_subset, on='간략 법정동주소', how='outer')
    df_house_infos.to_excel(doc_house_info_zone, index=False)

if False:
    # 선거인명부 개표결과 분석
    conf_poll_result = {
        "20대 총선": ['conf/개표결과-20대 총선 용인시갑.xlsx', 'conf/개표결과-20대 총선 용인시을.xlsx', 'conf/개표결과-20대 총선 용인시병.xlsx', 'conf/개표결과-20대 총선 용인시정.xlsx'],
        "21대 총선": ['conf/개표결과-21대 총선 용인시갑.xlsx', 'conf/개표결과-21대 총선 용인시을.xlsx', 'conf/개표결과-21대 총선 용인시병.xlsx', 'conf/개표결과-21대 총선 용인시정.xlsx'],
        "19대 대선": ['conf/개표결과-19대 대선 기흥구.xlsx', 'conf/개표결과-19대 대선 수지구.xlsx', 'conf/개표결과-19대 대선 처인구.xlsx']
    }
    conf_poll_book = {
        "20대 총선": ['conf/선거인수현황-20대 총선 기흥구.xlsx', 'conf/선거인수현황-20대 총선 수지구.xlsx', 'conf/선거인수현황-20대 총선 처인구.xlsx'],
        "21대 총선": ['conf/선거인수현황-21대 총선 기흥구.xlsx', 'conf/선거인수현황-21대 총선 수지구.xlsx', 'conf/선거인수현황-21대 총선 처인구.xlsx'],
        "19대 대선": ['conf/선거인수현황-19대 대선 기흥구.xlsx', 'conf/선거인수현황-19대 대선 수지구.xlsx', 'conf/선거인수현황-19대 대선 처인구.xlsx']
    }
    doc_poll_result = {}
    doc_poll_book = {}

    def iter_result(sg_id, file_ins):
        file_outs = []
        for file_in in file_ins[sg_id]:
            nec_result = nr.NecResult(sg_id, file_in)
            file_out = file_in.replace('conf/개표결과', 'doc/개표결과 정리')
            file_outs.append(file_out)
            nec_result.items.to_excel(file_out, index=False)
        return file_outs

    def iter_book(sg_id, file_ins):
        file_outs = []
        for file_in in file_ins[sg_id]:
            nec_book = np.NecPollbook(file_in)
            file_out = file_in.replace('conf/선거인수현황', 'doc/선거인수현황 정리')
            file_outs.append(file_out)
            nec_book.items.to_excel(file_out, index=False)
        return file_outs

    for sg_id in sg_ids:
        doc_poll_result[sg_id] = iter_result(sg_id, conf_poll_result)
        doc_poll_book[sg_id] = iter_book(sg_id, conf_poll_book)
    print(doc_poll_result)
    print(doc_poll_book)

    conf_sg_history = 'conf/총선 투표구 이력.xlsx'
    def rearrange_book(sg_id, file_ins):
        dfs = []
        for file_in in file_ins[sg_id]:
            df = pd.read_excel(file_in)
            dfs.append(df)
        df_from = pd.concat(dfs)

        sg_history = pd.read_excel(conf_sg_history)
        sg_history = sg_history[sg_history['선거'] == sg_id]
        print(sg_history)
        sg_zone = {}
        file_outs = []
        tpgs = sg_history['투표구'].unique()
        for tpg in tpgs:
            subset = sg_history[sg_history['투표구'] == tpg]
            hjds = subset['행정동'].unique()
            sg_zone[tpg] = hjds
            df_to = df_from[df_from['읍면동명'].isin(hjds)]
            if len(df_to.index) > 0:
                file_out = 'doc/선거인수현황 정리-' + sg_id + ' ' + tpg + '.xlsx'
                file_outs.append(file_out)
                df_to.to_excel(file_out, index=False)
        return file_outs

    for sg_id in sg_ids:
        if '총선' in sg_id:
            doc_poll_book[sg_id] = rearrange_book(sg_id, doc_poll_book)
    print(doc_poll_book)

if True:
    doc_poll_result = {
        "20대 총선": ['doc/개표결과 정리-20대 총선 용인시갑.xlsx', 'doc/개표결과 정리-20대 총선 용인시을.xlsx', 'doc/개표결과 정리-20대 총선 용인시병.xlsx', 'doc/개표결과 정리-20대 총선 용인시정.xlsx'],
        "21대 총선": ['doc/개표결과 정리-21대 총선 용인시갑.xlsx', 'doc/개표결과 정리-21대 총선 용인시을.xlsx', 'doc/개표결과 정리-21대 총선 용인시병.xlsx', 'doc/개표결과 정리-21대 총선 용인시정.xlsx'],
        "19대 대선": ['doc/개표결과 정리-19대 대선 기흥구.xlsx', 'doc/개표결과 정리-19대 대선 수지구.xlsx', 'doc/개표결과 정리-19대 대선 처인구.xlsx']
    }
    doc_poll_book = {
        "20대 총선": ['doc/선거인수현황 정리-20대 총선 용인시갑.xlsx', 'doc/선거인수현황 정리-20대 총선 용인시을.xlsx', 'doc/선거인수현황 정리-20대 총선 용인시병.xlsx', 'doc/선거인수현황 정리-20대 총선 용인시정.xlsx'],
        "21대 총선": ['doc/선거인수현황 정리-21대 총선 용인시갑.xlsx', 'doc/선거인수현황 정리-21대 총선 용인시을.xlsx', 'doc/선거인수현황 정리-21대 총선 용인시병.xlsx', 'doc/선거인수현황 정리-21대 총선 용인시정.xlsx'],
        "19대 대선": ['doc/선거인수현황 정리-19대 대선 기흥구.xlsx', 'doc/선거인수현황 정리-19대 대선 수지구.xlsx', 'doc/선거인수현황 정리-19대 대선 처인구.xlsx']
    }

if True:
    doc_poll_score = {}
    doc_poll_analysis = {}
    def iter_analysis(sg_id, file_results, file_books):
        file_scores = []
        file_analysises = []
        if len(file_results) == len(file_books):
            for index, file_result in enumerate(file_results):
                file_book = file_books[index]
                file_score = file_result.replace('개표결과 정리', '득표 현황')
                file_analysis = file_result.replace('개표결과 정리', '선거분석')
                file_scores.append(file_score)
                file_analysises.append(file_analysis)
                nec_analysis = na.NecAnalysis(file_result, file_book)
                nec_analysis.run(sg_id, doc_house_info_zone)
                nec_analysis.score.to_excel(file_score, merge_cells=False)
                nec_analysis.na.to_excel(file_analysis, merge_cells=False)
        return file_scores, file_analysises

    for sg_id in sg_ids:
        file_scores, file_analysises = iter_analysis(sg_id, doc_poll_result[sg_id], doc_poll_book[sg_id])
        doc_poll_score[sg_id] = file_scores
        doc_poll_analysis[sg_id] = file_analysises
    print(doc_poll_score)
    print(doc_poll_analysis)

    # if str(type(file_outs[sg_id])) == "<class 'str'>":
    # <class 'list'>
