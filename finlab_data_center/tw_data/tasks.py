# from etl.sql_interface import PickleUpdate
# from etl.git import git_init, git_commit, BASE_DIR
# import os
# import logging
#
# # Get an instance of a logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# base_path = BASE_DIR + '/tw_data'
# table_path = base_path + '/pickle_table/'
# tw_fdata_path = base_path + '/tw_fdata/'
#
#
# def divide_tw_pkl():
#     logger.info(base_path)
#     logger.info(table_path )
#     logger.info(tw_fdata_path)
#     git_init(work_dir=tw_fdata_path)
#     for t in ['stock_price', 'monthly_revenue', 'tej_fundamental']:
#         df = PickleUpdate().update_pkl(table_path, 'stock_data', t, pivot_data_path=tw_fdata_path)
#     git_commit()
#     return df
