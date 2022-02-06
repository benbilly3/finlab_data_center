from sqlalchemy import create_engine
import pandas as pd
import json5
import os
import datetime
import gc
import logging

# Get an instance of a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SqlData:
    """ Use raw sql and pandas get dataframe

    This interface could be used in general python env or djnago service(data-center).

    Attributes:
        base_dir(str): config file path,config file has db conncetion settings.
        db_name(str):db key in config file which you want to connect.
        django_env(bool):If it is true, develope env is in django framework.
    """

    def __init__(self, base_dir=os.path.dirname(os.path.abspath("__file__")), db_name='TW_DBNAME', django_env=True):
        self.db_name = db_name
        self.base_dir = base_dir
        self.django_env = django_env

    @staticmethod
    def _get_config(base_dir):

        with open(os.path.join(base_dir, "config.json"), encoding='utf8') as file:
            config = json5.load(file)
        return config

    def _create_engine(self):
        if self.django_env:
            from django.conf import settings
            db_name = (
                self.db_name
                if settings.CONFIG_DATA.get("PRODUCTION")
                else 'DEV_' + self.db_name
            )
            connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
                settings.CONFIG_DATA.get("DBACCOUNT"),
                settings.CONFIG_DATA.get("DBPASSWORD"),
                settings.CONFIG_DATA.get("DBHOST"),
                settings.CONFIG_DATA.get("DBPORT"),
                settings.CONFIG_DATA.get(db_name),
            )
        else:
            try:
                config = self._get_config(self.base_dir)
                connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
                    config.get("DBACCOUNT"),
                    config.get("DBPASSWORD"),
                    config.get("DBHOST"),
                    config.get("DBPORT"),
                    config.get(self.db_name),
                )
            except FileNotFoundError as error:
                logger.error(error)
                return None
        engine = create_engine(connect_info)

        return engine

    @staticmethod
    def _check_col_existed(conn, table, col):
        cursor = conn.execute(f"SHOW COLUMNS FROM `{table}` LIKE '{col}'")
        return list(cursor)

    def get(self, table, select_cols='*', limit=5, offset=0, data_format='pivot', all_data=False, index_col=None,
            stock_id=None,
            date_range=None, customized_query=None):

        """Select data.

        Args:
          table(str): A table name in db.
          select_cols(str): A str of selected columns ex('stock_id,date,close',default is '*'(select all columns)).
          limit(int): Select recent n days data
          offset(int): Skip the last n days.
          data_format(str): Format style enum[table','pivot'].
          all_data(bool):Get all data from table.If you want to get more
          index_col(list):Set Dataframe index_col.
          stock_id(str):Select stock_id range (ex:"('0050','0056')").
          date_range(str):Select date_range range (ex:"('2020-12-1','2020-11-30')").
          customized_query(str):Your customized sql code.

        Returns:
            table:DataFrame
            pivot:DataFrame in dict
            
        """

        #         tStart = time.time()
        conn = self._create_engine()
        try:
            if customized_query is None:
                if not self._check_col_existed(conn=conn, table=table, col='date') or all_data:
                    cursor = f"SELECT {select_cols} FROM {table}"
                else:
                    cursor = f"SELECT {select_cols} FROM {table} WHERE date IN (SELECT d.date FROM " \
                             f"(SELECT DISTINCT date FROM {table} ORDER BY date DESC" \
                             f" LIMIT {limit} OFFSET {offset}) as d)"
                    if date_range:
                        cursor = f"SELECT {select_cols} FROM {table} WHERE date IN {date_range}"
                    if stock_id:
                        cursor += f" and stock_id in {stock_id}"
            else:
                cursor = customized_query

            df = pd.read_sql(cursor, conn, index_col)
            if data_format is 'table':
                return df
            elif data_format is 'pivot':
                df = df.reset_index()
                df_cols = df.columns
                cols = [i for i in df_cols if i not in ['stock_id', 'date', 'index']]
                if 'date' not in df_cols:
                    msg = 'date column not in table, could not offer pivot format'
                    logger.error(msg)
                if len(cols) > 1:
                    pivot_set = {}
                    for c in cols:
                        table = pd.pivot_table(df, index=['date'], columns=['stock_id'], values=c)
                        pivot_set[c] = table
                else:
                    pivot_set = pd.pivot_table(df, index=['date'], columns=['stock_id'], values=cols[0])
                #                 tEnd = time.time()
                #                 print("It cost %f sec" % (tEnd - tStart))
                return pivot_set
        except Exception as error:
            logger.error(error)
            return None


class PickleUpdate:

    @classmethod
    def _get_path(cls, base_path, dir_name, table_name):
        path = base_path + dir_name + '/' + table_name + '.pkl'
        return path

    @classmethod
    def _get_update_date_range_str(cls, df):
        date = df['date'].values.max()
        pkl_edate = pd.to_datetime(str(date))
        now = datetime.datetime.now()

        if pkl_edate < now:
            update_date_range = tuple([i.strftime('%Y-%m-%d') for i in pd.date_range(start=pkl_edate, end=now)])
        else:
            update_date_range = tuple([i.strftime('%Y-%m-%d') for i in pd.date_range(start=pkl_edate, end=pkl_edate)])

        update_date_range_str = str(update_date_range)
        if len(update_date_range) < 2:
            update_date_range_str = update_date_range_str.replace(',', '')
        return update_date_range_str

    @classmethod
    def update_pkl(cls, base_path, dir_name, table_name, pivot_data_path=None):
        file_path = cls._get_path(base_path, dir_name, table_name)
        df = pd.read_pickle(file_path)
        data = SqlData()
        new_data = data.get(table=table_name, date_range=cls._get_update_date_range_str(df), data_format='table')
        result = pd.concat([df, new_data]).drop_duplicates(['stock_id', 'date'], keep='last')
        gc.collect()
        try:
            result.to_pickle(file_path)
            logger.info(f'success update {dir_name}/{table_name}.pkl')
            if pivot_data_path:
                df_cols = df.columns
                cols = [i for i in df_cols if i not in ['stock_id', 'date', 'index', 'id']]
                for c in cols:
                    if str(df[c].dtype) in ['float64', 'int64']:
                        pivot_df = pd.pivot_table(df, index=['date'], columns=['stock_id'], values=c, aggfunc='first')
                        pivot_df.to_pickle(pivot_data_path + f'/{c}.pkl')
                        # logger.info(f'divide pivot file:{c}')
                return 'Finish!success divide pivot file.'
        except Exception as e:
            logger.error(e)
            return e
