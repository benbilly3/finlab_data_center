import pandas as pd
from io import StringIO
import requests
from etl.utils import *
from etl.import_sql import create_connect_engine, table_latest_date
from tw_data.models import CompanyInfo, BrokerInfo, BrokerTrade, MonthlyRevenue
import time
import json
import numpy as np
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StockPriceCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股每日交易資訊"
        self.sub_market = ["sii", "otc", "rotc"]

    def crawl_sii(self):
        r = requests.post(
            "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=" + self.date_str + "&type=ALLBUT0999")
        content = r.text.replace("=", "")
        lines = content.split("\n")
        lines = list(filter(lambda l: len(l.split('",')) > 10, lines))
        content = "\n".join(lines)
        if content == "":
            return None
        df = pd.read_csv(StringIO(content))
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(",", ""))
        df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df["date"] = pd.to_datetime(self.date)
        df = df[["證券代號", "date", "證券名稱", "成交股數", "成交筆數", "成交金額", "開盤價", "收盤價", "最高價", "最低價", "最後揭示買價", "最後揭示賣價"]]

        df = df.rename(columns={"證券代號": "stock_id", "證券名稱": "stock_name",
                                "成交股數": "vol", "成交金額": "turnover_price",
                                "開盤價": "open", "收盤價": "close",
                                "最高價": "high", "最低價": "low", "成交筆數": "transactions_number",
                                "最後揭示買價": "finally_reveal_buy_price", "最後揭示賣價": "finally_reveal_sell_price"})
        return df

    @staticmethod
    def select_otc_id(code):
        if len(code) > 5:
            if code[-1] == "P":
                return False
            else:
                try:
                    code = int(code[:5])
                    if code > 10000:
                        return False
                    else:
                        return True
                except ValueError:
                    return True
        else:
            return True

    def crawl_otc(self):
        y = str(int(self.date.strftime("%Y")) - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        link = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=" \
               + date_str + "&s=0,asc,0"
        r = requests.get(link)
        lines = r.text.replace("\r", "").split("\n")
        try:
            df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
            df = df.astype(str)
        except pd.errors.ParserError:
            return None
        df.columns = list(map(lambda s: s.replace(" ", ""), lines[2].split(",")))
        df = df.apply(lambda s: s.str.replace(",", ""))
        df["stock_id"] = df["代號"]
        df["代號"] = df["代號"].apply(lambda s: self.select_otc_id(s))
        df = df[df["代號"]]
        df["date"] = pd.to_datetime(self.date)
        df = df[["stock_id", "date", "名稱", "成交股數", "成交金額(元)", "開盤", "收盤", "最高", "最低", "成交筆數", "最後買價", "最後賣價"]]
        df = df.rename(columns={"名稱": "stock_name",
                                "成交股數": "vol", "成交金額(元)": "turnover_price",
                                "開盤": "open", "收盤": "close",
                                "最高": "high", "最低": "low", "成交筆數": "transactions_number",
                                "最後買價": "finally_reveal_buy_price", "最後賣價": "finally_reveal_sell_price"})
        df.iloc[:, 3:] = df.iloc[:, 3:].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df = df.dropna(thresh=7)
        return df

    def crawl_rotc(self):
        link = "http://www.tpex.org.tw/web/emergingstock/historical/daily/EMDaily_dl.php?l=zh-tw&f=EMdes010." + \
               self.date_str + "-C.csv"
        r = requests.get(link)
        lines = r.text.replace("\r", "").split("\n")
        try:
            columns_line = lines[3]
        except IndexError:
            return None
        lines = list(filter(lambda l: len(l.split('",')) > 10, lines))
        try:
            df = pd.read_csv(StringIO("\n".join(lines)), header=None)
        except pd.errors.EmptyDataError:
            return None
        df.columns = list(map(lambda l: l.replace(" ", ""), columns_line.split(",")))
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(",", ""))
        df["date"] = pd.to_datetime(self.date)
        if "證券名稱" not in df.columns:
            df = df.rename(columns={"名稱": "證券名稱"})
            df['最後最佳報買價'] = None
            df['最後最佳報賣價'] = None

        df = df[["證券代號", "date", "證券名稱", "成交量", "成交金額", "前日均價", "最後", "最高", "最低", "日均價", "筆數", "最後最佳報買價", "最後最佳報賣價"]]
        df = df.rename(columns={"證券代號": "stock_id", "證券名稱": "stock_name",
                                "成交量": "vol", "成交金額": "turnover_price",
                                "前日均價": "open", "最後": "close",
                                "最高": "high", "最低": "low",
                                "日均價": "mean_price", "筆數": "transactions_number",
                                "最後最佳報買價": "finally_reveal_buy_price", "最後最佳報賣價": "finally_reveal_sell_price"})
        df.iloc[:, 3:] = df.iloc[:, 3:].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df['stock_id'] = df['stock_id'].apply(lambda s: s[:s.index('  ')] if '  ' in s else s)
        df['stock_name'] = df['stock_name'].apply(lambda s: s[:s.index('  ')] if '  ' in s else s)
        df = df[df["stock_id"] != "合計"]
        return df

    def crawl_main(self):
        try:
            df = pd.concat([self.crawl_sii(), self.crawl_otc()])
        except ValueError:
            return None
        return df


class MonthlyRevnueCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.target_name = "台股月營收資訊"
        self.sub_market = ["sii", "otc", "rotc"]

    def crawl_main(self):
        url_date = last_month(self.date)
        data = []
        for i in self.sub_market:
            url = 'https://mops.twse.com.tw/nas/t21/' + i + '/t21sc03_' + str(url_date.year - 1911) + '_' + str(
                url_date.month) + '.html'
            # 偽瀏覽器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/39.0.2171.95 Safari/537.36'}
            # 下載該年月的網站，並用pandas轉換成 dataframe
            try:
                r = requests.get(url, headers=headers)
                r.encoding = 'big5'
                html_df = pd.read_html(StringIO(r.text))
                # 處理一下資料
                if html_df[0].shape[0] > 500:
                    df = html_df[0].copy()
                else:
                    df = pd.concat([df for df in html_df if (df.shape[1] <= 11) and (df.shape[1] > 5)])

                if 'levels' in dir(df.columns):
                    df.columns = df.columns.get_level_values(1)
                else:
                    df = df[list(range(0, 10))]
                    column_index = df.index[(df[0] == '公司代號')][0]
                    df.columns = df.iloc[column_index]

                df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
                df = df[~df['當月營收'].isnull()]
                df = df[df['公司代號'] != '合計']
                df['date'] = datetime.date(self.date.year, self.date.month, 10)
                df = df.rename(columns={'公司代號': 'stock_id'})
                df = df.set_index(['stock_id', 'date'])
                data.append(df)
            except Exception as e:
                print(e)
                print(f'market:{i}**WARRN: Pandas cannot find any table in the HTML file')
                pass
        try:
            df = pd.concat(data, sort=False)
        except ValueError:
            return None
        if '備註' not in df.columns:
            df['備註'] = None
        df.iloc[:, 1:-1] = df.iloc[:, 1:-1].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df = df[df['公司名稱'] != '總計']
        df = df.where(pd.notnull(df), None)
        df = df.rename(columns={'公司名稱': "stock_name", "當月營收": "this_month_rev",
                                '上月營收': "last_month_rev", "去年當月營收": "last_year_rev",
                                '上月比較增減(%)': "cp_last_month_rev", "去年同月增減(%)": "cp_last_year_rev",
                                '當月累計營收': "cm_this_month_rev", "去年累計營收": "cm_last_year_rev",
                                '前期比較增減(%)': "cp_cm_rev", "備註": "note",
                                })
        df = df.reset_index()
        return df


class CompanyInfoCrawlerTW:
    def __init__(self):
        self.target_name = "台股企業基本資訊"
        self.sub_market = ["sii", "otc", "rotc"]

    def crawl_main(self):
        data = []
        market_category = self.sub_market
        for market in market_category:
            url = "https://mops.twse.com.tw/mops/web/ajax_t51sb01"
            form_data = {
                "encodeURIComponent": "1",
                "step": "1",
                "firstin": "1",
                "TYPEK": market
            }
            res = requests.post(url, data=form_data)
            res.encoding = "utf-8"
            df = pd.read_html(res.text)
            df = pd.DataFrame(df[0])
            df['market'] = market
            data.append(df)
        df2 = pd.concat(data, sort=False)
        df2 = df2.astype(str)
        df2 = df2.apply(lambda s: s.str.replace(",", ""))
        df3 = df2[["公司代號", "公司名稱", "公司簡稱", "產業類別", "外國企業註冊地國", "住址",
                   "董事長", "總經理", "發言人", "發言人職稱", "總機電話",
                   "成立日期", "上市日期", "上櫃日期", "興櫃日期", "實收資本額(元)", "已發行普通股數或TDR原發行股數",
                   "私募普通股(股)", "特別股(股)", "普通股盈餘分派或虧損撥補頻率", "股票過戶機構", "簽證會計師事務所",
                   "公司網址", "投資人關係聯絡電話", "投資人關係聯絡電子郵件", "英文簡稱", "market"]]
        df3 = df3.rename(columns={
            "公司代號": "stock_id", "公司名稱": "name",
            "公司簡稱": "short_name", "產業類別": "category",
            "外國企業註冊地國": "registered_country", "住址": "address",
            "董事長": "chairman", "總經理": "ceo",
            "發言人": "spokesman", "發言人職稱": "spokesman_title",
            "總機電話": "phone", "成立日期": "establishment_date",
            "上市日期": "sii_date", "上櫃日期": "otc_date",
            "興櫃日期": "rotc_date", "已發行普通股數或TDR原發行股數": "shares_issued",
            "私募普通股(股)": "private_shares", "特別股(股)": "special_shares",
            "普通股盈餘分派或虧損撥補頻率": "dividend_frequency", "股票過戶機構": "stock_transfer_institution",
            "簽證會計師事務所": "visa_accounting_firm", "公司網址": "website",
            "投資人關係聯絡電話": "investor_relations_contact", "投資人關係聯絡電子郵件": "investor_relations_email",
            "英文簡稱": "english_abbreviation", "實收資本額(元)": "capital"
        })
        # Data format Process
        df3 = df3[df3["stock_id"] != "公司代號"]
        df3["registered_country"] = df3["registered_country"].apply(lambda s: s.replace("－", "台灣"))
        for share_column in ["capital", "shares_issued", "private_shares", "special_shares"]:
            df3[share_column] = df3[share_column].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        for date_column in ["establishment_date", "sii_date", "otc_date", "rotc_date"]:
            df3[date_column] = df3[date_column].apply(lambda t: year_transfer(t))
        df3["update_time"] = datetime.datetime.now()
        df3 = df3.fillna('')
        return df3

    @staticmethod
    def update_xy():
        GetNTLSxy.update_xy_data(CompanyInfo)


class StockIndexPriceCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股指數資訊"
        self.sub_market = ["sii", "otc"]
        self.format = "time_series"

    def crawl_sii(self):

        r = requests.post(
            'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + self.date_str + '&type=IND')

        content = r.text.replace('=', '')
        lines = content.split('\n')
        lines = list(filter(lambda l: len(l.split('",')) > 5, lines))
        content = "\n".join(lines)
        if content == '':
            return None
        df = pd.read_csv(StringIO(content))
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df = df.rename(columns={'指數': 'stock_id', '收盤指數': 'index_price',
                                '漲跌百分比(%)': 'quote_change'})
        df['date'] = pd.to_datetime(self.date)
        df['stock_id'] = df['stock_id'].apply(lambda s: '上市' + s)
        df[['index_price', 'quote_change']] = df[['index_price', 'quote_change']].apply(
            lambda s: pd.to_numeric(s, errors='coerce'))

        df_all = df.loc[:, ['stock_id', 'date', 'index_price', 'quote_change']]
        df_all = df_all.dropna()

        return df_all

    def crawl_otc(self):

        y = str(int(self.date.strftime("%Y")) - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        link = 'http://www.tpex.org.tw/web/stock/aftertrading/index_summary/summary_download.php?l=zh-tw&d=' \
               + date_str + '&s=0,asc,0'
        r = requests.get(link)

        lines = r.text.replace("\r", "").split("\n")
        try:
            df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
        except pd.errors.ParserError:
            return None
        df.columns = list(map(lambda s: s.replace(" ", ""), lines[2].split(",")))
        df = df.apply(lambda s: s.str.replace(",", ""))

        df['stock_id'] = '上櫃' + (df['指數'].apply(lambda s: s.replace('指數', ''))) + '指數'

        # 第二個櫃買指數以下的才是報酬指數，找出第二個，各年指數項目不同使用find來定位
        rem_loc = df['指數'].str.find('櫃買指數')
        rem_loc = (rem_loc[rem_loc > -1].index.tolist())[-1]

        # 一般指數
        df_normal = df.iloc[:rem_loc]
        # 報酬指數
        df_rem = df.copy()
        df_rem = df_rem.iloc[rem_loc:]
        df_rem['stock_id'] = df_rem['stock_id'].apply(lambda s: s.replace('指數', '報酬指數'))
        #         合併
        df_all = pd.concat([df_normal, df_rem])
        df_all = df_all.rename(columns={'收市指數': 'index_price', '漲跌幅度': 'quote_change'})
        df_all[['index_price', 'quote_change']] = df_all[['index_price', 'quote_change']].apply(
            lambda s: pd.to_numeric(s, errors='coerce'))
        df_all['date'] = pd.to_datetime(self.date)
        df_all = df_all.loc[:, ['stock_id', 'date', 'index_price', 'quote_change']]
        df_all = df_all.dropna()
        return df_all

    def crawl_main(self):
        try:
            df = pd.concat([self.crawl_sii(), self.crawl_otc()])
        except ValueError:
            return None
        return df


class StockIndexVolCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股指數成交量資訊"
        self.sub_market = ["sii", "otc"]

    def sii_vol(self):
        r = requests.post('http://www.twse.com.tw/exchangeReport/BFIAMU?response=csv&date=' + self.date_str)
        content = r.text.replace('=', '')
        lines = content.split('\n')
        lines = list(filter(lambda l: len(l.split('",')) > 4, lines))
        content = "\n".join(lines)
        if content == '':
            return None
        df = pd.read_csv(StringIO(content))
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df = df.rename(
            columns={'分類指數名稱': 'stock_id', '成交股數': 'turnover_vol', '成交金額': 'turnover_price',
                     '成交筆數': 'turnover_num'})
        df['date'] = self.date
        df[['turnover_vol', 'turnover_price', 'turnover_num']] = df[['turnover_vol', 'turnover_price',
                                                                     'turnover_num']].apply(
            lambda s: pd.to_numeric(s, errors='coerce'))
        df = df.drop(columns=['漲跌指數', 'Unnamed: 5'])
        df['stock_id'] = df['stock_id'].apply(lambda s: '上市' + s)
        return df

    def sii_statistic(self):
        r = requests.post(
            'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + self.date_str + '&type=MS')
        content = r.text.replace('=', '')
        lines = content.split('\n')
        lines = list(filter(lambda l: len(l.split('",')) < 6, lines))
        lines = lines[1:]
        content = "\n".join(lines)
        if content == '':
            return None
        df = pd.read_csv(StringIO(content))
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df = df.rename(columns={'成交統計': 'stock_id', '成交金額(元)': 'turnover_price',
                                '成交股數(股)': 'turnover_vol', '成交筆數': 'turnover_num'})
        df = df.drop(columns={'Unnamed: 4'})
        df['date'] = self.date
        df.iloc[:, 1:4] = df.iloc[:, 1:4].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df = df.dropna()
        df['stock_id'] = df['stock_id'].apply(lambda s: '上市' + s[s.index(".") + 1:] if "." in s else '上市' + s)
        return df

    def otc_statistic(self):
        y = str(int(self.date.strftime("%Y")) - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        link = 'https://www.tpex.org.tw/web/stock/aftertrading/market_statistics/statistics_result.php?l=zh-tw&t=D&o=' \
               'htm&d=' + date_str
        r = requests.get(link)
        lines = r.text.replace("\r", "").split("\n")
        if len(lines) < 35:
            return None
        df = pd.read_html(StringIO("\n".join(lines[3:])))[0]
        df = pd.DataFrame(df)
        df.columns = df.columns.get_level_values(1)
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df = df.rename(columns={'成交統計': 'stock_id', '成交金額(元)': 'turnover_price',
                                '成交股數(股)': 'turnover_vol', '成交筆數': 'turnover_num'})
        df = df[['stock_id', 'turnover_vol', 'turnover_price', 'turnover_num']]
        df['date'] = self.date
        df.iloc[:, 1:4] = df.iloc[:, 1:4].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df = df.dropna()
        df['stock_id'] = df['stock_id'].apply(lambda s: '上櫃' + s[s.index(".") + 1:] if "." in s else '上櫃' + s)
        return df

    def crawl_main(self):
        try:
            df = pd.concat([self.sii_vol(), self.sii_statistic(), self.otc_statistic()], sort=False)
        except ValueError:
            return None
        return df


class BrokerInfoCrawler:
    def __init__(self):
        self.target_name = "台股券商資訊"

    @staticmethod
    def headquarter_info():
        r = requests.get('https://www.twse.com.tw/zh/brokerService/brokerServiceAudit')
        html_df = pd.read_html(StringIO(r.text))
        df = pd.DataFrame(html_df[0])
        df['department'] = '總公司'
        df = df.drop(columns='分公司')
        return df

    @staticmethod
    def branch_info(broker_hq_id):
        url = 'https://www.twse.com.tw/brokerService/brokerServiceAudit?showType=list&stkNo=' + broker_hq_id + \
              '&focus=6'
        r = requests.get(url)
        html_df = pd.read_html(StringIO(r.text))
        df = pd.DataFrame(html_df[3])
        return df

    def crawl_main(self):
        broker_hq = self.headquarter_info()
        branch_data = pd.concat([self.branch_info(i) for i in broker_hq['證券商代號'].values])
        branch_data['department'] = '分公司'
        df_all = pd.concat([broker_hq, branch_data])
        df_all = df_all.rename(columns={'證券商代號': 'stock_id', '證券商名稱': 'broker_name',
                                        '開業日': 'date_of_establishment', '地址': 'address',
                                        '電話': 'phone'
                                        })
        df_all = df_all[df_all['stock_id'] != '查無資料']
        df_all['date_of_establishment'] = df_all['date_of_establishment'].apply(lambda t: year_transfer(t))
        df_all['broker_name'] = df_all['broker_name'].apply(lambda s: s.replace(' ', '').replace('證券', ''))
        return df_all

    @staticmethod
    def update_xy():
        GetNTLSxy.update_xy_data(BrokerInfo)


class GetNTLSxy:
    @classmethod
    def get_xy(cls, address):
        for i in ['新竹科學工業園區', '新竹科學園區', '大發工業區',
                  '南部科學工業園區', '平鎮工業區', '高雄加工出口區'
                                       '南崗工業區']:
            address = address.replace(i, '')
        address = char_filter(address, '及', '部分', '、', ',', '（')
        # 解決郵遞區號問題
        filter_num = filter(str.isalpha, address[:7])
        address = ''.join(list(filter_num)) + address[7:]
        url = 'https://moisagis.moi.gov.tw/moiap/gis2010/content/user/matchservice/singleMatch.cfm'
        form = {
            'address': address,
            'matchRange': '0',
            'fuzzyNum': '0',
            'roadEQstreet': 'false',
            'subnumEQnum': 'false',
            'isLockTown': 'false',
            'isLockVillage': 'false',
            'ex_coor': 'EPSG:4326',
            'U02DataYear': '2015',
            'output_xml': '1'
        }
        try:
            r = requests.post(url, data=form)
            html_df = pd.read_html(StringIO(r.text))
        except ValueError:
            return None
        df = pd.DataFrame(html_df[0])
        df = df.where(pd.notnull(df), None)
        return df

    # 地址有些漏區的
    @classmethod
    def main_process(cls, address):
        df = cls.get_xy(address)
        if df is None:
            return None
        elif df['X'].values[0] is None:
            address = address[:3] + '信義區' + address[3:]
            df = cls.get_xy(address)
            return df
        else:
            return df

    # 更新table中經緯度資料,start、end控制更新範圍,only_null控制是否只爬空值
    @classmethod
    def update_xy_data(cls, model_name, start=None, end=None, only_null=True):
        bulk_update_data = []
        if only_null is True:
            obj_list = model_name.objects.filter(longitude__isnull=True)[start:end]
        else:
            obj_list = model_name.objects.all()
        for obj_check in obj_list:
            location = obj_check.address
            print(location, obj_check.id)
            df = cls.main_process(location)
            if df is None:
                print('pass')
                continue
            obj_check.city = df['縣市'].values[0]
            obj_check.district = df['鄉鎮'].values[0]
            obj_check.longitude = df['X'].values[0]
            obj_check.latitude = df['Y'].values[0]
            bulk_update_data.append(obj_check)
        update_fields_area = ['city', 'district', 'latitude', 'longitude']
        model_name.objects.bulk_update(bulk_update_data, update_fields_area, batch_size=1000)


class BrokerTradeCrawlerTW:

    def __init__(self, start_date):
        self.start_date = start_date
        self.start_date_str = start_date.strftime("%Y-%m-%d")
        self.target_name = "台股分點進出資訊"

    def check_trade_day(self):
        stock_range = StockPriceCrawlerTW(self.start_date)
        try:
            df = list(pd.concat([stock_range.crawl_sii(), stock_range.crawl_otc()])['stock_id'].values)
            return df
        except ValueError:
            return None

    def broker_trade(self, stock_id):
        # print(stock_id)
        url = 'https://fubon-ebrokerdj.fbs.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&e=' + self.start_date_str + \
              '&f=' + self.start_date_str
        r = requests.post(url)
        html_df = pd.read_html(StringIO(r.text))
        df = pd.DataFrame(html_df[2])
        # holiday
        if len(df) < 9:
            return None
        df.columns = df.iloc[5]
        if '合計買超股數' in df.iloc[:, :1].values:
            divide = 1000
        else:
            divide = 1
        buy_net_avg_cost = float(df[df['買超券商'] == '平均買超成本']['買超'].values[0])
        sell_net_avg_cost = float(df[df['賣超券商'] == '平均賣超成本']['賣超'].values[0])
        df = df.iloc[6:-3]
        buy_side = df.iloc[:, :5]
        buy_side = buy_side.rename(columns={'買超券商': 'broker_name', '買進': 'buy_num',
                                            '賣出': 'sell_num', '買超': 'net_bs',
                                            '佔成交比重': 'transactions_pt'})

        sell_side = df.iloc[:, 5:]
        sell_side = sell_side.rename(columns={'賣超券商': 'broker_name', '買進': 'buy_num',
                                              '賣出': 'sell_num', '賣超': 'net_bs',
                                              '佔成交比重': 'transactions_pt'})

        df_all = pd.concat([buy_side, sell_side], sort=False).dropna()

        df_all.iloc[:, 1:] = df_all.iloc[:, 1:].apply(lambda s: pd.to_numeric(s.str.replace('%', ''), errors="coerce"))
        df_all.iloc[:, 1:4] = df_all.iloc[:, 1:4] / divide
        df_all['net_bs'] = df_all['buy_num'] - df_all['sell_num']
        df_all['net_bs_cost'] = [i * buy_net_avg_cost if i > 0 else i * sell_net_avg_cost for i in df_all['net_bs']]
        df_all['date'] = pd.to_datetime(self.start_date)
        df_all['broker_name'] = df_all['broker_name'].apply(lambda s: s.replace('證券', '')).apply(
            lambda s: s.replace('(牛牛牛)', '犇'))
        df_all['stock_id'] = str(stock_id)
        return df_all

    def crawl_main(self):
        crawl_list = self.check_trade_day()
        # check holiday
        if crawl_list is not None:
            # check is new or old process
            new_obj = BrokerTrade.objects.filter(date=self.start_date_str)
            data = []
            if len(new_obj) > 0:
                table_last_day = table_latest_date(create_connect_engine(BrokerTrade), BrokerTrade._meta.db_table)
                finish_obj = BrokerTrade.objects.filter(date=table_last_day)
                last_stock_id = finish_obj[len(finish_obj) - 1].stock_id
                crawl_list = crawl_list[crawl_list.index(last_stock_id) + 1:]
            for stock_id in crawl_list:
                # self.broker_trade(stock_id)
                data.append(self.broker_trade(stock_id))
                # time.sleep(2.5)
            data = pd.concat(data)
            return data
        else:
            pass


class StockTiiCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股三大法人個股買賣超資訊"
        self.sub_market = ["sii", "otc", "rotc"]

    def crawl_sii(self):
        r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date=' + self.date_str + '&selectType=ALLBUT0999')
        try:
            df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
        except pd.errors.EmptyDataError:
            return None
        df = df.astype(str).apply(lambda s: s.str.replace(',', ''))
        df['證券代號'] = df['證券代號'].str.replace('=', '').str.replace('"', '')
        df[df.columns[2:]] = df[df.columns[2:]].apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all',
                                                                                                          axis=1)
        if self.date > datetime.datetime(2017, 12, 17):
            df = df.rename(columns={'證券代號': 'stock_id', '證券名稱': 'stock_name',
                                    '外陸資買進股數(不含外資自營商)': 'fm_buy', '外陸資賣出股數(不含外資自營商)': 'fm_sell',
                                    '外陸資買賣超股數(不含外資自營商)': 'fm_net', '外資自營商買進股數': 'fd_buy',
                                    '外資自營商賣出股數': 'fd_sell', '外資自營商買賣超股數': 'fd_net',
                                    '投信買進股數': 'itc_buy', '投信賣出股數': 'itc_sell',
                                    '投信買賣超股數': 'itc_net', '自營商買賣超股數': 'dealer_net',
                                    '自營商買進股數(自行買賣)': 'dealer_ppt_buy', '自營商賣出股數(自行買賣)': 'dealer_ppt_sell',
                                    '自營商買賣超股數(自行買賣)': 'dealer_ppt_net', '自營商買進股數(避險)': 'dealer_hedge_buy',
                                    '自營商賣出股數(避險)': 'dealer_hedge_sell', '自營商買賣超股數(避險)': 'dealer_hedge_net',
                                    '三大法人買賣超股數': 'tii_net'
                                    })
            df['ft_net'] = df['fm_net'] + df['fd_net']
        else:
            df = df.rename(columns={'證券代號': 'stock_id', '證券名稱': 'stock_name',
                                    '外資買進股數': 'fm_buy', '外資賣出股數': 'fm_sell',
                                    '外資買賣超股數': 'fm_net',
                                    '投信買進股數': 'itc_buy', '投信賣出股數': 'itc_sell',
                                    '投信買賣超股數': 'itc_net', '自營商買賣超股數': 'dealer_net',
                                    '自營商買進股數(自行買賣)': 'dealer_ppt_buy', '自營商賣出股數(自行買賣)': 'dealer_ppt_sell',
                                    '自營商買賣超股數(自行買賣)': 'dealer_ppt_net', '自營商買進股數(避險)': 'dealer_hedge_buy',
                                    '自營商賣出股數(避險)': 'dealer_hedge_sell', '自營商買賣超股數(避險)': 'dealer_hedge_net',
                                    '三大法人買賣超股數': 'tii_net'
                                    })
            df['ft_net'] = df['fm_net']
        df["date"] = pd.to_datetime(self.date)
        return df

    def crawl_otc(self):
        west_year = int(self.date.strftime("%Y"))
        y = str(west_year - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        r = requests.get(
            'http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=csv&se=EW&t=D&d='
            + date_str + '&s=0,asc')
        try:
            df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
        except pd.errors.ParserError:
            return None
        df = df.astype(str).apply(lambda s: s.str.replace(',', ''))
        df['代號'] = df['代號'].str.replace('=', '').str.replace('"', '')
        df[df.columns[2:]] = df[df.columns[2:]].apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all',
                                                                                                          axis=1)
        if self.date > datetime.datetime(2018, 1, 14):
            df = df.rename(columns={'代號': 'stock_id', '名稱': 'stock_name',
                                    '外資及陸資(不含外資自營商)-買進股數': 'fm_buy', '外資及陸資(不含外資自營商)-賣出股數': 'fm_sell',
                                    '外資及陸資(不含外資自營商)-買賣超股數': 'fm_net', '外資自營商-買進股數': 'fd_buy',
                                    '外資自營商-賣出股數': 'fd_sell', '外資自營商-買賣超股數': 'fd_net',
                                    '投信-買進股數': 'itc_buy', '投信-賣出股數': 'itc_sell',
                                    '投信-買賣超股數': 'itc_net', '自營商-買賣超股數': 'dealer_net',
                                    '自營商(自行買賣)-買進股數': 'dealer_ppt_buy', '自營商(自行買賣)-賣出股數': 'dealer_ppt_sell',
                                    '自營商(自行買賣)-買賣超股數': 'dealer_ppt_net', '自營商(避險)-買進股數': 'dealer_hedge_buy',
                                    '自營商(避險)-賣出股數': 'dealer_hedge_sell', '自營商(避險)-買賣超股數': 'dealer_hedge_net',
                                    '三大法人買賣超股數合計': 'tii_net'
                                    })
            df['ft_net'] = df['fm_net'] + df['fd_net']
            df = df.drop(columns=['外資及陸資-買進股數', '外資及陸資-賣出股數', '外資及陸資-買賣超股數', '自營商-買進股數', '自營商-賣出股數'])

        else:
            df = df.rename(columns={'代號': 'stock_id', '名稱': 'stock_name',
                                    '外資及陸資買股數': 'fm_buy', '外資及陸資賣股數': 'fm_sell',
                                    '外資及陸資淨買股數': 'fm_net',
                                    '投信買進股數': 'itc_buy', '投信賣股數': 'itc_sell',
                                    '投信淨買股數': 'itc_net', '自營淨買股數': 'dealer_net',
                                    '自營商(自行買賣)買股數': 'dealer_ppt_buy', '自營商(自行買賣)賣股數': 'dealer_ppt_sell',
                                    '自營商(自行買賣)淨買股數': 'dealer_ppt_net', '自營商(避險)買股數': 'dealer_hedge_buy',
                                    '自營商(避險)賣股數': 'dealer_hedge_sell', '自營商(避險)淨買股數': 'dealer_hedge_net',
                                    '三大法人買賣超股數': 'tii_net'
                                    })
            df['ft_net'] = df['fm_net']
        df["date"] = pd.to_datetime(self.date)
        return df

    def crawl_rotc(self):
        r = requests.get(
            'https://www.tpex.org.tw/web/emergingstock/historical/daily/EMDaily_dl.php?l=zh-tw&f=EMdss006.'
            + self.date_str + '-C.csv')
        try:
            df = pd.read_csv(StringIO(r.text), header=3).dropna(how='all', axis=1).dropna(how='any')
        except pd.errors.ParserError:
            return None
        df = df.drop(columns=['HEADER'])
        df = df.astype(str).apply(lambda s: s.str.replace(',', ''))
        try:
            df['證券代號'] = df['證券代號'].apply(lambda s: s[:4])
            df = df.rename(columns={'證券代號': 'stock_id', '證券名稱': 'stock_name',
                                    '外資(股數)': 'ft_net', '投信(股數)': 'itc_net',
                                    '自營商(股數)': 'dealer_net', '合計買賣超(股數)': 'tii_net',
                                    })
        except KeyError:
            df['股票代號'] = df['股票代號'].apply(lambda s: s[:4])
            df = df.rename(columns={'股票代號': 'stock_id', '名稱': 'stock_name',
                                    '外資': 'ft_net', '投信': 'itc_net',
                                    '自營商': 'dealer_net', '合計買賣超': 'tii_net',
                                    })
        df[df.columns[2:]] = df[df.columns[2:]].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df["date"] = self.date
        df['stock_id'] = df['stock_id'].apply(lambda s: s[:s.index(' ')] if '" "' in s else s)
        df['stock_name'] = df['stock_name'].apply(lambda s: s[:s.index(' ')] if '" "' in s else s)
        return df

    def crawl_main(self):
        try:
            df = pd.concat([self.crawl_sii(), self.crawl_otc(), self.crawl_rotc()], sort=False)
        except ValueError:
            return None
        return df


class StockTiiMarketCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股三大法人全市場日報資訊"
        self.sub_market = ["sii", "otc"]

    def crawl_sii(self):
        r = requests.get('http://www.twse.com.tw/fund/BFI82U?response=csv&dayDate=' + self.date_str + '&type=day')
        try:
            df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
        except pd.errors.EmptyDataError:
            return None
        df = df.astype(str).apply(lambda s: s.str.replace(',', ''))
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)

        df = df.rename(
            columns={'單位名稱': 'stock_id', '買進金額': 'buy_price',
                     '賣出金額': 'sell_price', '買賣差額': 'net'})
        df = df.set_index(['stock_id'])

        df = df.reset_index()
        df["date"] = self.date
        df['market'] = self.sub_market[0]
        return df

    def crawl_otc(self):
        y = str(int(self.date.strftime("%Y")) - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        r = requests.get(
            'http://www.tpex.org.tw/web/stock/3insti/3insti_summary/3itrdsum_result.php?l=zh-tw&o=csv&se=EW&t=D&p=0&d='
            + date_str + '&s=0,asc')
        try:
            df = pd.read_csv(StringIO(r.text), header=1)
        except pd.errors.ParserError:
            return None
        if len(df) < 3:
            return None
        df = df.astype(str).apply(lambda s: s.str.replace(',', '').str.replace('', ''))
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)
        df = df.rename(
            columns={'單位名稱': 'stock_id', '買進金額(元)': 'buy_price',
                     '賣出金額(元)': 'sell_price', '買賣超(元)': 'net'})
        df["date"] = self.date
        df['stock_id'] = [col.replace('\u3000', '') for col in df['stock_id']]
        df = df.set_index(['stock_id'])
        df = df.reset_index()
        df['market'] = self.sub_market[1]
        df = df.dropna(thresh=4)
        return df

    def crawl_main(self):
        try:
            df = pd.concat([self.crawl_sii(), self.crawl_otc()], sort=False)
        except ValueError:
            return None
        return df


class StockTdccCrawlerTW:
    def __init__(self):
        self.target_name = "台股集保餘額資訊"

    @classmethod
    def crawl_main(cls, file=False):
        if file is False:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1\
            0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            res = requests.get("https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5", headers=headers)
            df = pd.read_csv(StringIO(res.text))
        else:
            df = pd.read_csv(file)
        df = df.astype(str)
        df = df[~df['證券代號'].str.contains('YY|YE')]
        df = df.rename(columns={
            '證券代號': 'stock_id', '持股分級': 'hold_class',
            '人數': 'people', '股數': 'hold_num', '占集保庫存數比例%': 'hold_pt'
        })
        if 'hold_pt' not in df.columns:
            df = df.rename(columns={'佔集保庫存數比例%': 'hold_pt'})
        df = df[df['hold_class'] != '16']
        df.iloc[:, 2:6] = df.iloc[:, 2:6].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df['date'] = df[df.columns[0]].apply(lambda s: datetime.datetime.strptime(s, '%Y%m%d'))
        df = df.drop(columns=df.columns[0])
        return df


class StockMarginTransactionsCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股融資交易資訊"

    def crawl_sii(self):
        r = requests.get(
            'http://www.twse.com.tw/exchangeReport/MI_MARGN?response=csv&date=' + self.date_str + '&selectType=ALL')
        content = r.text.replace('=', '')
        lines = content.split('\n')
        lines = list(filter(lambda l: len(l.split('",')) > 10, lines))
        content = "\n".join(lines)
        if content == '':
            return None
        df = pd.read_csv(StringIO(content)).dropna(how='all', axis=1).dropna(thresh=15)
        if len(df) < 1:
            return None
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df['股票代號'] = df['股票代號'].apply(lambda s: '00' + s if len(s) < 3 else s)
        df = df.rename(columns={'股票代號': 'stock_id', '股票名稱': 'stock_name',
                                '買進': 'mt_buy', '賣出': 'mt_sell',
                                '現金償還': 'cash_redemption', '前日餘額': 'mt_balance_pd',
                                '今日餘額': 'mt_balance_now', '限額': 'mt_quota',
                                '買進.1': 'short_covering', '賣出.1': 'short_sale',
                                '現券償還': 'stock_redemption', '前日餘額.1': 'ss_balance_pd',
                                '今日餘額.1': 'ss_balance_now', '限額.1': 'ss_quota',
                                '資券互抵': 'offset', '註記': 'note'})
        df.iloc[:, 2:-1] = df.iloc[:, 2:-1].apply(lambda s: pd.to_numeric(s, errors='coerce'))

        df['note'] = [symbols_change(i, {'O': '停止融資', 'X': '停止融券', '@': '融資分配', '%': '融券分配', '!': '停止買賣'}) for i in
                      df['note']]
        df['mt_use_rate'] = [round(v / q * 100, 2) if q > 0 else 100 if v > 0 else 0 for v, q in
                             zip(df['mt_balance_now'], df['mt_quota'])]
        df['ss_use_rate'] = [round(v / q * 100, 2) if q > 0 else 100 if v > 0 else 0 for v, q in
                             zip(df['ss_balance_now'], df['ss_quota'])]
        df['date'] = self.date
        return df

    def crawl_otc(self):
        y = str(int(self.date.strftime("%Y")) - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        r = requests.get(
            'http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=csv&d='
            + date_str + '&s=0,asc,0')
        df = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(thresh=15)
        if len(df) < 10:
            return None
        df = df.astype(str).apply(lambda s: s.str.replace(',', ''))
        df.columns = [col.replace(' ', '') for col in df.columns]
        df['代號'] = df['代號'].apply(lambda s: '00' + s if len(s) < 3 else s)
        df = df.rename(columns={'代號': 'stock_id', '名稱': 'stock_name',
                                '資買': 'mt_buy', '資賣': 'mt_sell',
                                '現償': 'cash_redemption', '前資餘額(張)': 'mt_balance_pd',
                                '資餘額': 'mt_balance_now', '資限額': 'mt_quota',
                                '券買': 'short_covering', '券賣': 'short_sale',
                                '券償': 'stock_redemption', '前券餘額(張)': 'ss_balance_pd',
                                '券餘額': 'ss_balance_now', '券限額': 'ss_quota',
                                '資券相抵(張)': 'offset', '備註': 'note',
                                '資使用率(%)': 'mt_use_rate', '券使用率(%)': 'ss_use_rate'})
        df = df.drop(columns=['資屬證金', '券屬證金'])
        df.iloc[:, 2:-1] = df.iloc[:, 2:-1].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df['note'] = [symbols_change(i, {'O': '停止融資', 'X': '停止融券', '@': '融資分配', '%': '融券分配', '!': '停止買賣',
                                         '*': '融券餘額占融資餘額百分之六十以上者', 'A': '股價波動過度劇烈', 'B': '股權過度集中',
                                         'C': '成交量過度異常', 'D': '監視第二次處置'}) for i in df['note']]
        df['date'] = self.date
        return df

    def crawl_main(self):
        try:
            df = pd.concat([self.crawl_sii(), self.crawl_otc()], sort=False)
        except ValueError:
            return None
        return df


class Stock3PRatioCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.date_str = date.strftime("%Y%m%d")
        self.target_name = "台股個股PE,PB,殖利率數據"
        self.sub_market = ["sii", "otc"]
        self.format = "time_series"

    def crawl_sii(self):
        r = requests.get(
            'http://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=' + self.date_str + '&selectType=ALL')
        content = r.text.replace('=', '')
        lines = content.split('\n')
        lines = list(filter(lambda l: len(l.split('",')) > 5, lines))
        content = "\n".join(lines[:])
        if content == '':
            return None
        df = pd.read_csv(StringIO(content), header=0).dropna(how='all', axis=1)
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df = df[['證券代號', '證券名稱', '本益比', '殖利率(%)', '股價淨值比']]
        df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df = df.rename(
            columns={k: v for k, v in zip(df.columns, ['stock_id', 'stock_name', 'dividend_yield', 'pe', 'pb'])})
        df['date'] = self.date
        return df

    def crawl_otc(self):
        y = str(int(self.date.strftime("%Y")) - 1911)
        date_str = y + "/" + self.date.strftime("%m") + "/" + self.date.strftime("%d")
        link = 'https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_download.php?l=zh-tw&d=' \
               + date_str + '&s=0,asc,0'
        r = requests.get(link)
        lines = r.text.replace('\r', '').split('\n')
        if len(lines) < 10:
            return None
        df = pd.read_csv(StringIO("\n".join(lines[3:-1])), header=0)
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))
        df = df.drop(columns=['每股股利', '股利年度'])
        df = df.rename(
            columns={k: v for k, v in zip(df.columns, ['stock_id', 'stock_name', 'pe', 'dividend_yield', 'pb'])})
        df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda s: pd.to_numeric(s, errors='coerce'))
        df['date'] = self.date
        return df

    def crawl_main(self):
        try:
            df = pd.concat([self.crawl_sii(), self.crawl_otc()])
        except ValueError:
            return None
        return df


class InsiderHoldCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.target_name = "董 事 、 監 察 人 、 經 理 人 及 百 分 之 十 以 上 大 股 東 股 權 異 動 彙 總 表"
        self.sub_market = ["sii", "otc", "rotc"]

    def crawl_main(self):
        url_date = last_month(self.date)
        data = []
        for market in self.sub_market:
            # https://siis.twse.com.tw/publish/sii/95IRB110_10.HTM
            # https://mops.twse.com.tw/mops/web/IRB110
            url = 'https://siis.twse.com.tw/publish/' + market + '/' + str(
                url_date.year - 1911) + 'IRB110_' + url_month(url_date.month) + '.HTM'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/39.0.2171.95 Safari/537.36'}
            try:
                r = requests.get(url, headers=headers)
                r.encoding = 'big5'
                df = pd.read_html(r.text)[0].iloc[2:, :]
                data.append(df)
            except ValueError:
                print(print(f'market:{market}**WARRN: Pandas cannot find any table in the HTML file'))
                pass
        try:
            df = pd.concat(data)
        except ValueError:
            return None
        df = df.astype(str)
        df.columns = ['stock_name', 'issued_num', 'director_add', 'director_lower', 'director_hold',
                      'director_hold_ratio', 'manager_hold', 'big10_hold']
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df['stock_id'] = df['stock_name'].apply(lambda s: s[:4])
        df['stock_name'] = df['stock_name'].apply(lambda s: s[4:])
        df['date'] = datetime.date(self.date.year, self.date.month, 20)
        return df


class InsiderHoldDetailCrawlerTW:
    def __init__(self, date):
        self.date = date
        self.url_date = last_month(self.date)
        self.target_name = "董事、監察人、經理人及大股東持股月明細"
        self.sub_market = ["sii", "otc", "rotc"]

    def check_trade_day(self):
        month_date = self.date.strftime('%Y-%m-10')
        df = MonthlyRevenue.objects.filter(date=month_date).order_by('stock_id').values('stock_id')
        df = [v['stock_id'] for v in df]
        if len(df) > 0:
            return df
        else:
            return None

    def detail(self, stock_id, year, month):
        print(stock_id)
        url = 'https://mops.twse.com.tw/mops/web/ajax_stapap1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/39.0.2171.95 Safari/537.36'}
        res = requests.post(url, {
            'firstin': 'true',
            'year': year,
            'month': month,
            'co_id': stock_id,
            'step': '0'
        }, headers=headers
                            )
        try:
            df = pd.read_html(res.text)
        except Exception as e:
            print(e)
            return None
        try:
            table_loc = [i for i in range(len(df)) if len(df[i]) > 10][0]
        except Exception as e:
            print(e)
            return None
        df = df[table_loc]
        df = df[df[0] != '職稱']
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace("%", ""))
        df.columns = ['title', 'name', 'act_hold', 'hold', 'pledge',
                      'pledge_ratio', 'family_hold', 'family_pledge', 'family_pledge_ratio']
        df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df['stock_id'] = stock_id
        df['date'] = datetime.date(self.date.year, self.date.month, 20)
        return df

    def crawl_main(self):
        crawl_list = self.check_trade_day()
        year = self.url_date.year - 1911
        month = self.url_date.month
        # check holiday
        if crawl_list is not None:
            data = []
            for stock_id in crawl_list:
                data.append(self.detail(stock_id, year, month))
                time.sleep(3)
            return data
        else:
            pass


class StockDivideRatioCrawlerTW:
    def __init__(self):
        self.target_name = "台股股價還原表"
        self.format = "time_series"
        self.year = datetime.datetime.now().year

    @staticmethod
    def otc_date():
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        y = str(y - 1911)
        m = str(m) if m > 9 else '0' + str(m)
        d = str(d) if d > 9 else '0' + str(d)
        datestr = '%s/%s/%s' % (y, m, d)
        return datestr

    def twse_divide_ratio(self):
        datestr = datetime.datetime.now().strftime('%Y%m%d')
        res = requests.get(
            "https://www.twse.com.tw/exchangeReport/TWT49U?response=csv&strDate=" + str(self.year) + "0101&endDate=" \
            + datestr + "&_=1651532565786")
        df = pd.read_csv(StringIO(res.text.replace("=", "")), header=1)
        df = df.dropna(thresh=5).dropna(how='all', axis=1)
        df = df[~df['資料日期'].isnull()]
        # set stock id
        df['stock_id'] = df['股票代號']
        # set dates
        df = df[~df['資料日期'].isnull()]
        years = df['資料日期'].str.split('年').str[0].astype(int) + 1911
        years.loc[df['資料日期'].str[3] != '年'] = np.nan
        years.loc[years > datetime.datetime.now().year] = np.nan
        years.ffill(inplace=True)
        dates = years.astype(int).astype(str) + '/' + df['資料日期'].str.split('年').str[1].str.replace('月',
                                                                                                   '/').str.replace('日',
                                                                                                                    '')
        df['date'] = pd.to_datetime(dates, errors='coerce')
        # convert to float
        float_name_list = ['除權息前收盤價', '除權息參考價', '權值+息值', '漲停價格',
                           '跌停價格', '開盤競價基準', '減除股利參考價', '最近一次申報每股 (單位)淨值',
                           '最近一次申報每股 (單位)盈餘']
        df[float_name_list] = df[float_name_list].astype(str).apply(lambda s: s.str.replace(',', '')).astype(float)
        df['divide_ratio'] = df['除權息前收盤價'] / df['開盤競價基準']
        df = df.drop(columns=['資料日期', '股票代號', '漲停價格', '跌停價格', '詳細資料', '最近一次申報資料 季別/日期',
                              '最近一次申報每股 (單位)淨值', '最近一次申報每股 (單位)盈餘', '減除股利參考價'])
        df.columns = ['stock_name', 'divide_before', 'divide_after', 'divide_value', 'divide_category', 'divide_open',
                      'stock_id', 'date', 'divide_ratio']
        return df

    def otc_divide_ratio(self):
        res_otc = requests.get(
            'https://www.tpex.org.tw/web/stock/exright/dailyquo/exDailyQ_result.php?l=zh-tw&d=' + str(
                self.year - 1911) + '/01/01&ed='
            + self.otc_date() + '&_=1651594269115')
        df = pd.DataFrame(json.loads(res_otc.text)['aaData'])
        df.columns = ['除權息日期', '代號', '名稱', '除權息前收盤價', '除權息參考價',
                      '權值', '息值', "權+息值", "權/息", "漲停價格",
                      "跌停價格", "開盤競價基準", "減除股利參考價", "現金股利", "每千股無償配股",
                      "現金增資股數", "現金增資認購價", "公開承銷股數", "員工認購股數", "原股東認購數", "按持股比例千股認購"]
        float_name_list = ['除權息前收盤價', '除權息參考價',
                           '權值', '息值', "權+息值", "漲停價格", "跌停價格", "開盤競價基準",
                           "減除股利參考價", "現金股利", "每千股無償配股", "現金增資股數", "現金增資認購價",
                           "公開承銷股數", "員工認購股數", "原股東認購數", "按持股比例千股認購"
                           ]
        df[float_name_list] = df[float_name_list].astype(str).apply(lambda s: s.str.replace(',', '')).astype(float)
        # set stock id
        df['stock_id'] = df['代號']
        # set dates
        dates = df['除權息日期'].str.split('/')
        dates = (dates.str[0].astype(int) + 1911).astype(str) + '/' + dates.str[1] + '/' + dates.str[2]
        df['date'] = pd.to_datetime(dates)
        df['divide_ratio'] = df['除權息前收盤價'] / df['開盤競價基準']
        df = df.drop(columns=['除權息日期', '代號', '權值', '息值', '漲停價格', '跌停價格', '減除股利參考價', '現金股利',
                              '每千股無償配股', '現金增資股數',
                              '現金增資認購價', '公開承銷股數', '員工認購股數', '原股東認購數', '按持股比例千股認購'])
        df.columns = ['stock_name', 'divide_before', 'divide_after', 'divide_value', 'divide_category', 'divide_open',
                      'stock_id', 'date', 'divide_ratio']
        return df

    def twse_cap_reduction(self):
        datestr = datetime.datetime.now().strftime('%Y%m%d')
        res3 = requests.get(
            "https://www.twse.com.tw/exchangeReport/TWTAUU?response=csv&strDate=" + str(self.year) + "0101&endDate="
            + datestr + "&_=1651597854043")
        df = pd.read_csv(StringIO(res3.text), header=1)
        df = df.dropna(thresh=5).dropna(how='all', axis=1)
        dates = (df['恢復買賣日期'].str.split('/').str[0].astype(int) + 1911).astype(str) + df['恢復買賣日期'].str[3:]
        df['date'] = pd.to_datetime(dates, errors='coerce')
        df['stock_id'] = [s[:s.index('.')] if '.' in s else s for s in df['股票代號'].astype(str)]
        df['開盤競價基準'] = [a if a > 0 else b for a, b in zip(df['開盤競價基準'], df['恢復買賣參考價'])]
        df['divide_ratio'] = df['停止買賣前收盤價格'] / df['開盤競價基準']
        df = df.drop(columns=['恢復買賣日期', '股票代號', '漲停價格', '跌停價格', '詳細資料'])
        df.columns = ['stock_name', 'divide_before', 'divide_after', 'divide_open', 'divide_value', 'divide_category',
                      'date', 'stock_id', 'divide_ratio']
        df['divide_value'] = None
        return df

    def otc_cap_reduction(self):
        res4 = requests.get(
            "https://www.tpex.org.tw/web/stock/exright/revivt/revivt_result.php?l=zh-tw&d=" + str(
                self.year - 1911) + "/01/01&ed="
            + self.otc_date() + "&_=1651611342446")
        df = pd.DataFrame(json.loads(res4.text)['aaData'])
        name = ['恢復買賣日期', '股票代號', '股票名稱', '最後交易之收盤價格',
                '減資恢復買賣開始日參考價格', '漲停價格', '跌停價格', '開始交易基準價', '除權參考價', '減資源因', '詳細資料']
        float_name_list = ['最後交易之收盤價格', '減資恢復買賣開始日參考價格', '漲停價格', '跌停價格', '開始交易基準價', '除權參考價']
        df.columns = name
        df[float_name_list] = df[float_name_list].astype(str).apply(lambda s: s.str.replace(',', '')).astype(float)
        df['stock_id'] = df['股票代號'].astype(str)
        dates = (df['恢復買賣日期'].astype(str).str[:-4].astype(int) + 1911).astype(str) + \
                df['恢復買賣日期'].astype(str).str[-4:]
        df['date'] = pd.to_datetime(dates, errors='coerce')
        df['開始交易基準價'] = [a if a > 0 else b for a, b in zip(df['開始交易基準價'], df['減資恢復買賣開始日參考價格'])]
        df['divide_ratio'] = df['最後交易之收盤價格'] / df['開始交易基準價']
        df = df.drop(columns=['恢復買賣日期', '股票代號', '漲停價格', '跌停價格', '詳細資料'])
        df.columns = ['stock_name', 'divide_before', 'divide_after', 'divide_open', 'divide_value', 'divide_category',
                      'stock_id', 'date', 'divide_ratio']
        df['divide_value'] = None
        return df

    def crawl_main(self):
        df = pd.concat(
            [self.twse_divide_ratio(), self.otc_divide_ratio(), self.twse_cap_reduction(),
             self.otc_cap_reduction()], sort=False)
        df = df[df['divide_ratio'] > 0]
        return df


class InsiderShareholdingDeclarationTransferCrawlerTW:
    def __init__(self):
        self.target_name = "台股內部人持股轉讓宣告"
        self.sub_market = ["sii", "otc", "rotc"]

    def crawl_func(self, market, year, smonth='01', emonth='12'):
        # https://mops.twse.com.tw/mops/web/t56sb21_q3
        url = 'https://mops.twse.com.tw/mops/web/ajax_t56sb21'
        form_data = {'encodeURIComponent': '1',
                     'run': 'Y',
                     'step': '1',
                     'TYPEK': market,
                     'year': year,
                     'smonth': smonth,
                     'emonth': emonth,
                     'sstep': '1',
                     'firstin': 'true'}
        res = requests.post(url, data=form_data)
        res.encoding = 'utf-8'
        df = pd.read_html(StringIO(res.text))[0]
        df.columns = [a if a == b else a + '_' + b for a, b in df.columns]
        df = df.astype(str)
        df = df.rename(columns={
            '申報日期': 'date',
            '公司代號': 'stock_id',
            '公司名稱': 'stock_name',
            '申報人身分': 'declarant_identity',
            '姓名': 'name',
            '預定轉讓方式及股數_轉讓方式': 'shares_transfer_method',
            '預定轉讓方式及股數_轉讓股數': 'transferred_shares_num',
            '每日於盤中交易最大得轉讓股數': 'maximum_transferable_shares_in_one_day',
            '受讓人': 'assignee',
            '目前持有股數_自有持股': 'current_shares',
            '目前持有股數_保留運用決定權信託股數': 'current_shares_trust',
            '預定轉讓總股數_自有持股': 'transferred_own_shares_total_num',
            '預定轉讓總股數_保留運用決定權信託股數': 'transferred_trust_shares_total_num',
            '預定轉讓後持股_自有持股': 'after_transfer_own_shareholding',
            '預定轉讓後持股_保留運用決定權信託股數': 'after_transfer_trust_shareholding',
            '是否申報持股未完成轉讓': 'declare_uncompleted_transfer'})

        df['date'] = df['date'].apply(lambda t: year_transfer(t, method='datetime'))
        df['有效轉讓期間'] = df['有效轉讓期間'].apply(lambda t: t.replace('nan', '000/01/01 ~ 000/01/01'))
        df['start_date'] = df['有效轉讓期間'].apply(lambda t: year_transfer(t[:t.index('~') - 1], method='datetime'))
        df['end_date'] = df['有效轉讓期間'].apply(lambda t: year_transfer(t[t.index('~') + 1:], method='datetime'))
        df['declare_uncompleted_transfer'] = df['declare_uncompleted_transfer'].apply(
            lambda t: t.replace('是', '1').replace('nan', '0'))
        df = df.drop(columns=['異動情形', '有效轉讓期間'])
        numeric_col = ['transferred_shares_num', 'maximum_transferable_shares_in_one_day', 'current_shares',
                       'current_shares_trust', 'transferred_own_shares_total_num', 'transferred_trust_shares_total_num',
                       'after_transfer_own_shareholding', 'after_transfer_trust_shareholding',
                       'declare_uncompleted_transfer']
        df[numeric_col] = df[numeric_col].apply(lambda s: pd.to_numeric(s, errors="coerce"))
        df['market'] = market
        df = df.sort_values('date')
        return df

    def crawl_main(self, y_list=None):
        if y_list is None:
            year = datetime.datetime.now().year - 1911
            y_list = [str(year)]
        try:
            data = []
            for m in self.sub_market:
                for y in y_list:
                    try:
                        df = self.crawl_func(m, y)
                    except Exception as e:
                        logger.error(m, e)
                        return None
                    data.append(df)
                    time.sleep(10)
            result = pd.concat(data).sort_values('date')
        except Exception as e:
            logger.error(e)
            return None
        return result
