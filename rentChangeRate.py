import pandas as pd


class RentChageRate:
    def __init__(self, conf_rent_change_rate):
        self.items = pd.read_excel(conf_rent_change_rate)
        self.items.set_index('지역(3)', inplace=True)

        texts = self.items.columns.values[-1].split('. ')
        self._last_year = int(texts[0])
        self._last_month = int(texts[1])

        print('한국감정원 전월세 전환율 데이터: 2011.1 ~', self._last_year, '.', self._last_month)
        print(self.items)

    def _validate_ym(self, year, month):
        if month < 1:
            month = 1
        elif month > 12:
            month = 12

        if year < 2011:
            year = 2011
            month = 1
        elif year > self._last_year:
            year = self._last_year
            month = self._last_month
        elif year == self._last_year:
            if month > self._last_month:
                month = self._last_month

        return year, month

    def get(self, gu_name, year_in, month_in):
        year, month = self._validate_ym(year_in, month_in)
        ym = str(year) + '. ' + str(month).zfill(2)
        rate = self.items.loc[gu_name, ym]
        # print(gu_name, ym, rate)

        return rate
