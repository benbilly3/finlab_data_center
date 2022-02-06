import logging
from etl.import_sql import SqlImporter, CrawlerProcess
from us_data.crawlers import *
from us_data.models import *
from tw_data.stock_crawlers import *
from tw_data.models import *
from etl.notifications import EmailNotification

logging.basicConfig(level=logging.INFO)


def crawler_task(crawler, func, model, date_range, use_date_list=False, time_sleep=20, jump_update=False,
                 directly_create=False, check_date_rule=True, fk_columns=False):
    crawler = CrawlerProcess(eval(crawler), func, eval(model), date_range, use_date_list=use_date_list,
                             time_sleep=time_sleep, jump_update=jump_update, directly_create=directly_create,
                             check_date_rule=check_date_rule, fk_columns=fk_columns)
    return crawler.auto_update_crawl()


def crawler_task_once(crawler, func, model, directly_create=False, jump_update=False, check_date_rule=True,
                      fk_columns=False):
    df = getattr(eval(crawler)(), func)()
    importer = SqlImporter.add_to_sql(eval(model), df, directly_create=directly_create, jump_update=jump_update,
                                      check_date_rule=check_date_rule, fk_columns=fk_columns)
    return importer


def crawlers_daily_report_email_notification():
    df = EmailNotification.push_crawlers_processed_report()
    return df


def django_q_hook(task):
    """""
    hook func
    """""
    print(task.result)
