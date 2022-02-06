import quandl
from django.conf import settings
import pandas as pd
from etl.import_sql import create_connect_engine, get_connect_db_name
from us_data.models import SharaderSp500, IndexComponents
from io import StringIO
import requests
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SharadarCrawler:
    def __init__(self, date=None):
        self.date = date
        quandl.ApiConfig.api_key = settings.CONFIG_DATA.get("QUANDL_API_KEY")

    def download_sep(self):
        df = quandl.get_table('SHARADAR/SEP', date=self.date, paginate=True)
        if len(df) < 1:
            return None
        df = df.drop(columns='lastupdated')
        df = df.rename(columns={'ticker': 'stock_id'})
        return df

    def download_sp500(self):
        engine = create_connect_engine(SharaderSp500)
        conn = engine.connect()
        db_name=get_connect_db_name(SharaderSp500)
        sql = f"DELETE FROM {db_name}.sharader_sp500"
        conn.execute(sql)
        df = quandl.get_table('SHARADAR/SP500', paginate=True)
        if len(df) < 1:
            return None
        df = df.drop(columns='note')
        df = df.rename(columns={'ticker': 'stock_id'})
        df = df.replace({'N/A': None})
        df = df[df['action'] == 'current']
        df['id'] = [i for i in range(1, len(df) + 1)]
        return df

    def download_sf1(self):
        df = quandl.get_table('SHARADAR/SF1', calendardate=self.date, paginate=True)
        if len(df) < 1:
            return None
        df = df.rename(columns={'ticker': 'stock_id', "calendardate": 'date'})
        return df

    def download_sf3a(self):
        df = quandl.get_table('SHARADAR/SF3A', calendardate=self.date, paginate=True)
        if len(df) < 1:
            return None
        df = df.rename(columns={'ticker': 'stock_id', "calendardate": 'date'})
        return df

    def download_sf3b(self):
        df = quandl.get_table('SHARADAR/SF3B', calendardate=self.date, paginate=True)
        if len(df) < 1:
            return None
        df = df.rename(columns={'calendardate': 'date'})
        return df

    def download_actions(self):
        df = quandl.get_table('SHARADAR/actions', date=self.date, paginate=True)
        if len(df) < 1:
            return None
        df = df.rename(columns={'ticker': 'stock_id', 'calendardate': 'date'})
        df = df.replace({'N/A': None})
        return df

    def download_daily(self):
        df = quandl.get_table('SHARADAR/DAILY', date=self.date, paginate=True)
        if len(df) < 1:
            return None
        df = df.drop(columns='lastupdated')
        df = df.rename(columns={'ticker': 'stock_id'})
        return df

    def download_eventcodes(self):
        df = quandl.get_table('SHARADAR/EVENTCODES', paginate=True)
        if len(df) < 1:
            return None
        #         df=df.rename(columns={'ticker': 'stock_id','calendardate':'date'})
        #         df=df.replace({'N/A': None})
        return df

    def download_tickers(self):
        df = quandl.get_table('SHARADAR/TICKERS', paginate=True)
        if len(df) < 1:
            return None
        return df


class SlickchartsCrawler:
    def __init__(self, date=None):
        self.market_range = ['dowjones', 'nasdaq100', 'sp500']

    def index_components(self, index_name: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.75 Safari/537.36'}
        # dowjones,nasdaq100,sp500
        try:
            url = f"https://www.slickcharts.com/{index_name}"
        except Exception as error:
            logger.error(error)
            df = pd.DataFrame()
            return df
        r = requests.get(url, headers=headers)
        df = pd.read_html(StringIO(r.text))[0]
        df = df.rename(columns={'Company': 'name', 'Symbol': 'stock_id', 'Weight': 'weight'})
        df = df[['stock_id', 'name', 'weight']]
        df['index_name'] = index_name
        return df

    def main(self):
        try:
            df = pd.concat([self.index_components(i) for i in self.market_range])
            df['id'] = [i for i in range(1, len(df) + 1)]
        except Exception as error:
            logger.error(error)
            return None
        engine = create_connect_engine(IndexComponents)
        conn = engine.connect()
        sql = f"DELETE FROM dev_us_data.index_components"
        conn.execute(sql)
        return df
