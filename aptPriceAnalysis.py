import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os


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
        self.dStart = datetime.datetime(start_year, start_month, 1)
        self.dEnd = datetime.datetime(end_year, end_month, end_day)

    def analysis(self, addr):
        texts = addr.strip().split(' ')
        is_bjd = self.deal_price_all['법정동'] == texts[0]
        is_num = self.deal_price_all['지번'] == texts[1]
        deal_prices = self.deal_price_all[is_bjd & is_num].reset_index(drop=True)

        deal_prices['date'] = ''
        for i in range(deal_prices.index.size):
            deal_prices.at[i, 'date'] = datetime.datetime(deal_prices.at[i, '년'], deal_prices.at[i, '월'], deal_prices.at[i, '일'])
        print(deal_prices)

        temp1 = deal_prices.drop_duplicates(subset=['전용면적'], ignore_index=True)
        temp2 = temp1.sort_values(by=['전용면적'], ascending=False)
        area_sizes = temp2['전용면적']
        print(area_sizes.values)

        fig, ax = plt.subplots()
        for area_size in area_sizes.values:
            print(area_size)
            is_size = deal_prices['전용면적'] == area_size
            plot_data = deal_prices[is_size][['date', '거래금액']].reset_index(drop=True)
            ax.scatter(plot_data['date'], plot_data['거래금액']/10000, label=area_size, s=30, alpha=0.8, edgecolors='none', zorder=3)
            plt.xlim(self.dStart, self.dEnd)
            plt.xlabel('Year-Month')
            plt.ylabel('Price')
            plt.xticks(fontsize=7)
            plt.xticks(rotation=45)
            plt.interactive(True)
            ax.grid(True, zorder=0, color='#cccccc', linewidth=0.2)
            ax.legend()
            plt.show()
            plt.savefig(self.chart)

