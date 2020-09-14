# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import aptList as apt

import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
service_key = 'wRaEeY%2BpbPZX3OjIYLLt74uO5%2BAY7DXQJ9MWyyGodai94K7JvfjtLL%2FTRzkFuMxfb6SmuGqcM2YSCcVa4V1KeQ%3D%3D'
service_key = requests.utils.unquote(service_key)

callback_url = 'http://apis.data.go.kr/1611000/AptListService/getLegaldongAptList'

aptList = apt.AptList(callback_url, service_key)

bjd_file = './conf/yi_bjd_code.txt'
target_dongs = ['동백동', '중동', '마북동', '보정동']
aptList.get(bjd_file, target_dongs)
print(aptList.items)
