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

conf_yi_elecplace_file = 'conf/용인시 투표구 관할구역.xlsx'
conf_yi_elecplace_sheet = '2020년 제21대 국회의원선거'

conf_yiaddr_file = 'conf/용인시 통리반 관할구역.xlsx'
conf_yiaddr_sheet = 'step1'
conf_yiaddr_file_fix = 'conf/용인시 통리반 관할구역-수정.xlsx'

doc_kapt_info = 'doc/KAPT 공동주택 현황.xlsx'
conf_kapt_info_fix = 'conf/KAPT 공동주택 현황-수정.xlsx'

doc_house_info = 'doc/공동주택 현황.xlsx'
doc_poll_addr_list = 'doc/투표구 관할주소.xlsx'
doc_poll_house_list = 'doc/투표구 관할단지.xlsx'
doc_trade_price = 'doc/주택 매매 현황.xlsx'
doc_rent_price = 'doc/주택 임대차 현황.xlsx'

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

if False:
    house_info = hi.HouseInfo(conf_yiapt_list_file, conf_yiapt_list_sheet, doc_kapt_info, conf_kapt_info_fix)
    house_info.run()
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
    poll_addr = npa.NecPollAddress(conf_yi_elecplace_file, conf_yi_elecplace_sheet)
    poll_addr.run()
    poll_addr.to_excel(doc_poll_addr_list)

if False:
    poll_house = nph.NecPollHouse(conf_yiaddr_file, conf_yiaddr_sheet, conf_yiaddr_file_fix, doc_house_info, doc_poll_addr_list)
    poll_house.run()
    poll_house.to_excel(doc_poll_house_list)

if True:
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
    doc_poll_house_info = 'doc/투표구 관할단지 정보.xlsx'
    df_house_infos.to_excel(doc_poll_house_info)

    house_price_analysis = hpa.HousePriceAnalysis(doc_trade_price, start_year, start_month, end_year, end_month)
    house_price_analysis.analysis('중동 874', 'doc/img/', '기흥구 중동 874 백현마을동일하이빌 매매')

if True:
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

if True:
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
    nr_file = '선거통계/[제21대_국회의원선거]_개표단위별_개표결과-용인시정.xlsx'
    nec_result = nr.NecResult()
    nec_result.open(nr_file)

    np_file = '선거통계/[제21대_국회의원선거]_선거인명부_확정상황-기흥구.xlsx'
    nec_pollbook = np.NecPollbook()
    nec_pollbook.open(np_file)

    nec_result_part = nec_result.items[['읍면동투표구명', '읍면동명', '투표구명', '선거인수', '투표수', '기권수']].copy()
    nec_result_part.rename(columns={'읍면동명': '읍면동명_결과', '투표구명': '투표구명_결과'}, inplace=True)
    nec_analysis = pd.merge(nec_pollbook.items, nec_result_part, on='읍면동투표구명', how='right')
    nec_analysis['선거일 투표수'] = ''
    nec_analysis['사전선거 투표수'] = nec_analysis['확정된 국내선거인수 (A)'] - nec_analysis['선거인수']

    def day_voter(x):
        result = ''
        if x['사전선거 투표수'] > 0:
            result = x['투표수']
        return result
    nec_analysis['선거일 투표수'] = nec_analysis.apply(day_voter, axis=1)

    nec_analysis.drop(nec_analysis.index[nec_analysis['투표구명'] == '소계'], axis=0, inplace=True)
    dongs = nec_analysis['읍면동명'].dropna().unique()
    nec_analysis.set_index(['읍면동명_결과', '투표구명_결과'], inplace=True)
    nec_analysis['관내사전투표수'] = ''
    for dong in dongs:
        dong_pre_sum = nec_analysis.loc[(dong, '관내사전투표'), '선거인수']
        dong_pre = nec_analysis.loc[dong, '사전선거 투표수'].sum()
        dong_pre_in_ratio = dong_pre_sum / dong_pre
        for place in nec_analysis.loc[dong].index:
            nec_analysis.loc[(dong, place), '관내사전투표수'] = \
                nec_analysis.loc[(dong, place), '사전선거 투표수'] * dong_pre_in_ratio
    nec_analysis['관외사전투표수'] = nec_analysis['사전선거 투표수'] - nec_analysis['관내사전투표수']

    nec_analysis['선거일 투표율'] = nec_analysis['선거일 투표수'] / nec_analysis['확정된 국내선거인수 (A)'] * 100
    nec_analysis['사전선거 투표율'] = nec_analysis['사전선거 투표수'] / nec_analysis['확정된 국내선거인수 (A)'] * 100
    nec_analysis['관내사전선거 투표율'] = nec_analysis['관내사전투표수'] / nec_analysis['확정된 국내선거인수 (A)'] * 100
    nec_analysis['사전선거중 관내비중'] = nec_analysis['관내사전투표수'] / nec_analysis['사전선거 투표수'] * 100
    nec_analysis['투표율'] = nec_analysis['선거일 투표율'] + nec_analysis['사전선거 투표율']
    nec_analysis['기권율'] = nec_analysis['기권수'] / nec_analysis['확정된 국내선거인수 (A)'] * 100
    nec_analysis.drop(nec_analysis.index[pd.isna(nec_analysis['투표구명'])], axis=0, inplace=True)

    nec_score = nec_result.items.copy()
    nec_score.drop('읍면동투표구명', axis=1, inplace=True)
    nec_score['유형'] = '선거일투표'
    score = []

    nec_score.set_index(['읍면동명', '투표구명', '유형'], inplace=True)
    for dong in dongs:
        dong_pre_score = nec_score.loc[(dong, '관내사전투표', '선거일투표')].copy()
        dong_pre_sum = dong_pre_score['선거인수']
        for place in nec_analysis.loc[dong].index:
            place_pre_sum = nec_analysis.loc[(dong, place), '관내사전투표수']
            place_pre_score = dong_pre_score / dong_pre_sum * place_pre_sum
            place_pre_score.rename((dong, place, '관내사전투표'), inplace=True)
            score.append(place_pre_score)

    gu_pre_sum_analysis = nec_analysis['관외사전투표수'].sum()
    gu_pre_out_score = nec_score.loc[('거소·선상투표', '전체', '선거일투표')]
    gu_pre_out_score = gu_pre_out_score.add(nec_score.loc[('관외사전투표', '전체', '선거일투표')])
    gu_pre_out_score = gu_pre_out_score.add(nec_score.loc[('국외부재자투표', '전체', '선거일투표')])
    gu_pre_out_score = gu_pre_out_score.add(nec_score.loc[('잘못 투입·구분된 투표지', '전체', '선거일투표')])
    gu_pre_sum = gu_pre_out_score['선거인수']

    for dong in dongs:
        for place in nec_analysis.loc[dong].index:
            place_pre_sum = nec_analysis.loc[(dong, place), '관외사전투표수']
            place_pre_score = gu_pre_out_score / gu_pre_sum_analysis * place_pre_sum
            place_pre_score.rename((dong, place, '관외사전투표'), inplace=True)
            score.append(place_pre_score)

    nec_score = nec_score.append(score)
    nec_score.drop(['거소·선상투표', '관외사전투표', '국외부재자투표', '잘못 투입·구분된 투표지'], axis=0, level=0, inplace=True)
    nec_score.drop(['소계', '관내사전투표'], axis=0, level=1, inplace=True)
    nec_score.sort_index(inplace=True)
    print(nec_score.loc[('국외부재자투표(공관)', '전체', '선거일투표'), '투표수'])
    total_valid = nec_score['투표수'].sum() - nec_score.loc[('국외부재자투표(공관)', '전체', '선거일투표'), '투표수']

    stat_score = []
    analysis_total_ratio = []
    analysis_ratio = []
    for dong in dongs:
        for place in nec_analysis.loc[dong].index:
            place_score = nec_score.loc[(dong, place)]
            score_sum = place_score.sum()
            score_sum.rename((dong, place, '소계'), inplace=True)

            score_ratio = score_sum / score_sum['투표수'] * 100
            score_ratio_analysis = score_ratio.copy()
            score_total_ratio_anlaysis = score_sum / total_valid * 100 * nec_analysis.index.size
            score_ratio.rename((dong, place, '비율'), inplace=True)
            score_ratio_analysis.rename((dong, place), inplace=True)
            score_total_ratio_anlaysis.rename((dong, place), inplace=True)

            stat_score.append(score_sum)
            stat_score.append(score_ratio)
            analysis_ratio.append(score_ratio_analysis)
            analysis_total_ratio.append(score_total_ratio_anlaysis)

    nec_score = nec_score.append(stat_score)
    nec_score.sort_index(inplace=True)
    nec_score.to_excel('nec_score.xlsx')

    df_ratio = pd.DataFrame(analysis_ratio)
    df_ratio.drop(['선거인수', '투표수'], axis=1, inplace=True)
    df_total_ratio = pd.DataFrame(analysis_total_ratio)
    df_total_ratio.drop(['선거인수', '투표수'], axis=1, inplace=True)

    nec_analysis = pd.concat([nec_analysis, df_ratio], axis=1)
    nec_analysis = pd.concat([nec_analysis, df_total_ratio], axis=1)
    nec_analysis.to_excel('nec_anlysis.xlsx')
