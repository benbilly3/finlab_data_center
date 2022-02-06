import datetime
import time
import pandas as pd
from dateutil.rrule import rrule, DAILY, MONTHLY
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from sqlalchemy import create_engine
from django.db import models
import logging
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)


# """""
# DB connection
# """""

def get_connect_db_name(model: object):
    db_name = model._meta.app_label
    db_name = (
        db_name
        if settings.CONFIG_DATA.get("PRODUCTION")
        else 'dev_' + db_name
    )
    return db_name


def create_connect_engine(model: object):
    db_name = get_connect_db_name(model)
    connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        os.getenv('DBACCOUNT', settings.CONFIG_DATA.get("DBACCOUNT")),
        os.getenv('DBPASSWORD', settings.CONFIG_DATA.get("DBPASSWORD")),
        os.getenv('DBHOST', settings.CONFIG_DATA.get("DBHOST")),
        os.getenv('DBPORT', settings.CONFIG_DATA.get("DBPORT")),
        db_name,
    )
    engine = create_engine(connect_info)
    return engine


# """""
# date generator
# """""


def date_range(start_date, end_date):
    return [dt for dt in rrule(DAILY, dtstart=start_date, until=end_date)]


def month_range(start_date):
    return [dt for dt in rrule(MONTHLY, dtstart=start_date, count=2)]


# """""
# Table check tools
# """""


def table_exist(conn, table):
    return list(conn.execute(
        "select count(*) from information_schema.tables where TABLE_NAME=" + "'" + table + "'"))[0][0] == 1


def table_latest_date(conn, table):
    try:
        cursor = list(conn.execute('SELECT date FROM ' + table + ' ORDER BY date DESC LIMIT 1;'))
        return cursor[0][0]
    except IndexError:
        logger.error("No Data in table,start to init import table.")


def table_earliest_date(conn, table):
    try:
        cursor = list(conn.execute('SELECT date FROM ' + table + ' ORDER BY date ASC LIMIT 1;'))
        return cursor[0][0]
    except IndexError:
        info = "No Data in table,start to init import table."
        logger.error(info)
        return info


def in_date_list(conn, model_name: object, check_date):
    table = model_name._meta.db_table
    cursor = list(conn.execute("SELECT date FROM " + table + " where date ='" + check_date + "'"))
    try:
        if len(cursor) > 0:
            return True
        else:
            return False
    except IndexError:
        info = "No Data in table,start to init import table."
        logger.error(info)
        return info


class SqlImporter:
    """""
    Dataframe匯入DB,適用時間序列資料,fk_columns-外鍵對應過濾用欄位名
    """""

    @classmethod
    def get_fk_field_names(cls, model_name: object):
        fk_field_names = [field.name for field in model_name._meta.fields
                          if isinstance(field, models.ForeignKey)]
        return fk_field_names

    @classmethod
    def corr_obj(cls, model_name: object, attributes):
        try:
            df = model_name.objects.get(**attributes)
            return df
        except ObjectDoesNotExist:
            pass

    @classmethod
    def fk_import(cls, model_name: object, df, fk_columns):
        fk_field_names = cls.get_fk_field_names(model_name)
        fk_remote_model = [model_name._meta.get_field(i).remote_field.model for i in fk_field_names]
        filter_dict = [{a: df[b] for a, b in sub_dict.items()} for sub_dict in fk_columns]
        fk_obj = [cls.corr_obj(m, n) for m, n in zip(fk_remote_model, filter_dict)]
        data = {'fk_field_names': fk_field_names, 'fk_obj': fk_obj}
        return data

    @classmethod
    def fk_create(cls, model_name: object, df, fk_columns):
        data = cls.fk_import(model_name, df, fk_columns)
        fk_create_data = dict((m, n) for m, n in zip(data['fk_field_names'], data['fk_obj']))
        return fk_create_data

    @classmethod
    def fk_update(cls, model_name: object, df, fk_columns):
        data = cls.fk_import(model_name, df, fk_columns)
        return zip(data['fk_field_names'], data['fk_obj'])

    @classmethod
    def pk_select(cls, df, pk_columns):
        get_pk_dict = {pk: df[pk] for pk in pk_columns}
        get_pk_contain_dict = {pk + '__contains': df[pk] for pk in pk_columns}
        return [get_pk_dict, get_pk_contain_dict]

    @classmethod
    def add_to_sql(cls, model_name: object, df, directly_create=False, jump_update=False, check_date_rule=True,
                   fk_columns=False):
        if df.empty:
            info = f'Fail!df is empty'
            logger.error(info)
            return info
        df = df.where(pd.notnull(df), None)
        try:
            pk_columns = list(model_name._meta.unique_together[0])
        except IndexError:
            pk_columns = ['stock_id']
        df = df.drop_duplicates(pk_columns, keep='first')

        columns_list = list(df.columns.values)
        bulk_update_data = []
        bulk_create_data = []

        def bulk_create_func(bc_model_name, bc_columns_list, item):
            obj_create_data = dict((field, item[field]) for field in bc_columns_list)
            # 處理ForeignKey
            if fk_columns:
                obj_create_data.update(cls.fk_create(model_name, item, fk_columns))
            obj_create = bc_model_name(**obj_create_data)
            bulk_create_data.append(obj_create)

        # if date isn't in table,process bulk_create
        if check_date_rule:
            if 'date' in columns_list:
                data_date = df['date'].iloc[0].strftime('%Y-%m-%d')
                check_date = in_date_list(create_connect_engine(model_name), model_name, data_date)
            else:
                check_date = True
        else:
            check_date = False
        if check_date is False:
            # Change CSV to iterrow
            for index, item in df.iterrows():
                try:
                    bulk_create_func(model_name, columns_list, item)
                except Exception as e:
                    logger.error(f"error{' '}{e}{' '}Stock_id:{item['stock_id']}")
                    pass
        else:
            if directly_create:
                info = 'Finish update work'
                return info
            else:
                if jump_update:
                    # 已存在日期中的資料，過濾stock_id，直接create，不做update
                    exist_obj = model_name.objects.filter(date=df['date'].iloc[0]).values_list('stock_id', flat=True)
                    exist_obj = list(set(exist_obj))

                    df = df[~df['stock_id'].isin(exist_obj)]
                    if len(df) == 0:
                        return None
                    # Change CSV to iterrow
                    for index, item in df.iterrows():
                        try:
                            bulk_create_func(model_name, columns_list, item)
                        except Exception as e:
                            logger.error(f"error{' '}{e}{' '}Stock_id:{item['stock_id']}")
                            pass
                else:
                    for index, item in df.iterrows():
                        # Use bulk_update to update obj,PS:must include primary key column
                        try:
                            pk_filter = cls.pk_select(item, pk_columns)
                            try:
                                obj_check = model_name.objects.get(**pk_filter[0])
                            # 無法區分字母大小寫,回傳2個值
                            except MultipleObjectsReturned:
                                obj_check = model_name.objects.get(**pk_filter[1])

                            attribute_data = columns_list
                            update_data = [item[field] for field in columns_list]
                            for attribute, update_value in zip(attribute_data, update_data):
                                setattr(obj_check, attribute, update_value)
                            # ForeignKey update
                            if fk_columns:
                                for attribute, update_value in cls.fk_update(model_name, item, fk_columns):
                                    setattr(obj_check, attribute, update_value)
                            bulk_update_data.append(obj_check)
                        # Use dict to bulk_create obj when get nothing ,process incomplete data
                        except ObjectDoesNotExist:
                            bulk_create_func(model_name, columns_list, item)
                        except Exception as e:
                            logger.error(f"error{' '}{e}{' '}Stock_id:{item['stock_id']}")
                            pass

        # Process bulk
        model_name.objects.bulk_create(bulk_create_data)
        if 'date' in columns_list:
            date_list = sorted(list(set(df['date'].values.tolist())))
            download_date_range = [date_list[0], date_list[-1]]
            download_date_range = [datetime.datetime.fromtimestamp(t / 1e9).strftime('%Y-%m-%d') for t in
                                   download_date_range]
            logger.info_date = f"from{' '}{download_date_range[0]}{' '}to{' '}{download_date_range[1]}"
        else:
            download_date_range = datetime.datetime.now().strftime('%Y-%m-%d')
            logger.info_date = f"from{' '}{download_date_range}{' '}to{' '}{download_date_range}"

        bulk_create_info = f"Finish!{model_name}{' '}date:{logger.info_date}{' '}bulk_create:" \
                           f"{len(bulk_create_data)}"

        logger.info(bulk_create_info)

        update_fields_area = [field.name for field in model_name._meta.fields if field.name != 'id']
        model_name.objects.bulk_update(bulk_update_data, update_fields_area)
        bulk_update_info = f"Finish!{model_name}{' '}date:{logger.info_date}{' '}" \
                           f"bulk_update:{len(bulk_update_data)}"
        logger.info(bulk_update_info)
        all_info = bulk_create_info + ',' + bulk_update_info
        return all_info


class CrawlerProcess:
    """""
    爬蟲執行物件,適用時間序列資料
    Attributes:
    crawl_class-爬蟲類別、crawl_method-類別執行方法、model_name-存取資料庫模型、date_range-爬蟲日期產生器週期選擇
    time_sleep-爬蟲間隔時間
    fk_columns-外鍵對應過濾用欄位名[{'關聯表對應值':'本表對應值'}]
    use_date_list-直接爬整個date_list範圍,quandl適用
    """""

    def __init__(self, crawl_class: object, crawl_method: str, model_name: object, date_range, use_date_list=False,
                 time_sleep=13, jump_update=False, directly_create=False, check_date_rule=True, fk_columns=False):
        self.crawl_class = crawl_class
        self.crawl_method = crawl_method
        self.model_name = model_name
        self.table_earliest_date = table_earliest_date(create_connect_engine(model_name),
                                                       self.model_name._meta.db_table)
        self.table_latest_date = table_latest_date(create_connect_engine(model_name),
                                                   self.model_name._meta.db_table)
        self.date_range = date_range
        self.time_sleep = time_sleep
        self.pk_columns = list(self.model_name._meta.unique_together[0])
        self.fk_columns = fk_columns
        self.directly_create = directly_create
        self.jump_update = jump_update
        self.check_date_rule = check_date_rule
        self.use_date_list = use_date_list

    def __repr__(self):
        return str(self.model_name._meta.db_table) + ' ' + "\ntable_earliest_date:" + str(
            self.table_earliest_date) + "\ntable_latest_date:" + str(self.table_latest_date)

    def crawl_process(self, date_list: list):
        info_process = 'Finish update work'
        if self.use_date_list:
            df = getattr(self.crawl_class(date_list), self.crawl_method)()
            try:
                SqlImporter.add_to_sql(self.model_name, df, self.directly_create,
                                       self.jump_update, self.check_date_rule, self.fk_columns)
                info_process = f"Finish!download data from{' '}{date_list[0]}{' '}to{' '}{date_list[-1]}"
                logger.info(info_process)
            # holiday is blank
            except AttributeError:
                info_process = f"Fail!check if{' '}{date_list[0]}{' '}to{' '}{date_list[-1]}{' '}is holidays"
                logger.info(info_process)
        else:
            for d in date_list:
                df = getattr(self.crawl_class(d), self.crawl_method)()
                try:
                    SqlImporter.add_to_sql(self.model_name, df, self.directly_create,
                                           self.jump_update, self.check_date_rule, self.fk_columns)
                    daily_info = f"Finish!download data from{' '}{d}{' '}to{' '}{d}"
                    info_process = f"Finish!download data from{' '}{date_list[0]}{' '}to{' '}{date_list[-1]}"
                    logger.info(daily_info)
                # holiday is blank
                except AttributeError:
                    info_process = f'Fail!check if {d} is a holiday'
                    logger.error(info_process)
                time.sleep(self.time_sleep)
        return info_process

    def _monthly(self, start_date, end_date, deadline):
        """""
        deadline為每月最後執行爬蟲日，防止多餘更新動作
        """""
        table_latest_month = self.table_latest_date.month
        date_list = month_range(start_date)
        if end_date.month == table_latest_month:
            date_list = date_list[:1]
            if end_date.day > deadline:
                info = f"Finish!this month update work,month_crawler deadline is {deadline}"
                logger.info(info)
                return info

        elif end_date.month != table_latest_month:
            date_list = date_list[1:]

        logger.info(date_list)

        return date_list

    def us_seasonly(self, start_date=None, end_date=None, now=True):
        if now:
            present_year = datetime.datetime.now()
            datelist = pd.date_range(str(present_year.year - 1), str(present_year.year + 1), freq='Q').astype(
                str).to_list()
        else:
            datelist = pd.date_range(str(start_date.year - 1), str(end_date.year + 1), freq='Q').astype(str).to_list()
        return datelist[2:]

    # 指定區間，主要為初始化table和測試用
    def specified_date_crawl(self, start_date: str, end_date: str, deadline=0):
        global info, date_list
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        try:
            if (start_date - end_date).days <= 0:
                if self.date_range == 'date_range':
                    date_list = date_range(start_date, end_date)
                elif self.date_range == 'month_range':
                    date_list = self._monthly(start_date, end_date, deadline)
                elif self.date_range == 'us_season_range':
                    date_list = self.us_seasonly(start_date, end_date, now=False)
                else:
                    info = f"Finish!update work in past"
                    logger.warning(info)
                return self.crawl_process(date_list)
            else:
                info = f"Fail!The start_date > your end_date,please modify your start_date <={end_date}."
                logger.error(info)
                return info
        except Exception as error:
            logger.error(error)
            return error

    # 進度判斷
    def working_process(self, start_date, end_date):
        day_num = (end_date - start_date).days
        if day_num > 0:
            return 0
        elif day_num == 0:
            return 1
        else:
            return -1

    # 自動爬取結尾後日期的資料,jump－跳過最近日更新
    def auto_update_crawl(self, last_day='Now', deadline=15, jump=True):
        global date_list
        try:
            if last_day == 'Now':
                end_date = datetime.datetime.now()
            else:
                end_date = datetime.datetime.strptime(last_day, "%Y-%m-%d")
            start_date = self.table_latest_date
            working_process = self.working_process(start_date, end_date)
            if working_process == 0:
                if self.date_range == 'date_range':
                    # [1:] avoid same index,let program be faster
                    date_list = date_range(start_date, end_date)
                    if jump is True:
                        date_list = date_list[1:]
                elif self.date_range == 'month_range':
                    date_list = self._monthly(start_date, end_date, deadline)
                    # last_date > deadline
                    if type(date_list) is str:
                        return date_list
                elif self.date_range == 'us_season_range':
                    date_list = self.us_seasonly()
                return self.crawl_process(date_list)
            elif working_process == 1:
                if self.date_range == 'month_range':
                    date_list = self._monthly(start_date, end_date, deadline)
                elif self.date_range == 'us_season_range':
                    date_list = self.us_seasonly()
                    return self.crawl_process(date_list)
                info = "Finish update work"
                logger.warning(info)
                return info
            elif working_process == -1:
                if self.date_range == 'month_range':
                    date_list = self._monthly(start_date, end_date, deadline)
                    return self.crawl_process(date_list)
                if self.date_range == 'us_season_range':
                    date_list = self.us_seasonly()
                    return self.crawl_process(date_list)
                info = f"Fail!The table_latest_date > your setting date,please modify your setting date >{last_day}."
                logger.error(info)
                return info
        except Exception as error:
            logger.error(error)
            return error


def batchly_import_df(df, model, range_: int):
    total = len(df) + range_
    num_list = [i for i in range(0, total, range_)]
    for s, e in zip(num_list[:-1], num_list[1:]):
        sub_df = df.iloc[s:e]
        SqlImporter.add_to_sql(model, sub_df, check_date_rule=False)
