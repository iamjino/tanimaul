# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import aptList as al
import aptInfo as ai
import elecPlace as ep
import aptInfoMerge as ai2
import elecCode as el
import pandas as pd
import openpyxl

import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Tanimaul')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
service_key = 'wRaEeY%2BpbPZX3OjIYLLt74uO5%2BAY7DXQJ9MWyyGodai94K7JvfjtLL%2FTRzkFuMxfb6SmuGqcM2YSCcVa4V1KeQ%3D%3D'
service_key = requests.utils.unquote(service_key)

if False:
    # Get Apt List
    aptList = al.AptList(service_key)

    bjd_file = './conf/용인시 법정동 코드.txt'
    # target_gus = []
    target_gus = ['기흥구', '수지구', '처인구']
    target_dongs = ['동백동']
    # target_dongs = ['동백동', '중동', '마북동', '보정동']
    aptList.get(bjd_file, target_gus, target_dongs)
    print(aptList.items)

    # Get Apt Info
    aptInfo = ai.AptInfo(service_key)
    print(aptInfo.items)

    apt_codes = aptList.items['단지코드']
    # apt_codes = ['A44691615', 'A44679103']
    print(apt_codes)

    aptInfo.get(apt_codes)

    # apt_infos = pd.concat(aptList.items, aptInfo.items, axis=1)
    apt_infos = pd.merge(aptList.items, aptInfo.items, on='단지코드')
    # apt_infos['단지명 일치'] = apt_infos['단지명'] == apt_infos['단지명2']
    apt_infos.to_excel('공동주택 현황.xlsx', sheet_name='code')
    print(apt_infos)

if True:
    apt_info2 = ai2.AptInfoMerge()
    apt_info2.run()

if False:
    # elec_list = el.ElecCode(service_key)
    # elec_list.get()
    # print(elec_list.items)
    # elec_list.items.to_excel('elecCode_sg.xlsx', sheet_name='sg')
    elec_place = ep.ElecPlace()
    elec_place.decode()
    print(elec_place.items)
    elec_place.items.to_excel('투표구 관할구역.xlsx', sheet_name='place')

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
