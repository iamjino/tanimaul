import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager
import numpy as np


class AptPriceAnalysis:
    def __init__(self, doc_apt_price, price_chart, start_year, start_month, end_year, end_month):
        self.deal_price_all = pd.read_excel(doc_apt_price)

        self.chart = price_chart
        if os.path.isfile(self.chart):
            os.remove(self.chart)

        end_day = 31
        if end_month == 2:
            end_day = 28
        elif end_month in [4, 6, 9, 11]:
            end_day = 30
        self.start_year = start_year
        self.dStart = datetime.datetime(start_year, start_month, 1)
        self.dEnd = datetime.datetime(end_year, end_month, end_day)

    def _font_list_checker(self):
        font_manager._rebuild()
        for font in font_manager.fontManager.ttflist:
            if 'Nanum' in font.name:
                print(font.name, font.fname)

    def analysis(self, addr):
        texts = addr.strip().split(' ')
        is_dong = self.deal_price_all['법정동'] == texts[0]
        is_jibun = self.deal_price_all['지번'] == texts[1]
        deal_prices = self.deal_price_all[is_dong & is_jibun].reset_index(drop=True)

        deal_prices['date'] = ''
        for i in range(deal_prices.index.size):
            deal_prices.at[i, 'date'] = datetime.datetime(deal_prices.at[i, '년'], deal_prices.at[i, '월'], deal_prices.at[i, '일'])

        area_sizes = np.sort(deal_prices['전용면적'].unique())[::-1]
        # print(area_sizes, type(area_sizes))

        if deal_prices.size > 0:
            build_year = deal_prices.at[0, '건축년도']
            print(build_year)
            if self.start_year < build_year:
                self.dStart = datetime.date(build_year, 1, 1)

        plt.rcParams['font.family'] = 'NanumBarunGothicOTF'
        fig, ax = plt.subplots()
        plt.interactive(True)
        plt.xlim(self.dStart, self.dEnd)
        plt.xlabel('계약년월')
        plt.ylabel('실거래가 (억 원)')
        plt.xticks(fontsize=7, rotation=45)
        plt.yticks(fontsize=7)
        ax.grid(True, zorder=0, color='#cccccc', linewidth=0.2)

        for area_size in area_sizes:
            is_size = deal_prices['전용면적'] == area_size
            area_size = round(area_size, 3)
            print(area_size)
            plot_data = deal_prices[is_size][['date', '거래금액']]
            ax.scatter(plot_data['date'], plot_data['거래금액']/10000, label=area_size, s=20, alpha=0.8, edgecolors='none', zorder=3)

        ax.legend(fontsize='xx-small', title='전용면적(㎡)', title_fontsize='x-small')
        plt.show()
        plt.savefig(self.chart)
