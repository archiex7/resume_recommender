import argparse
import pandas as pd
import os
import sys
from pathlib import Path
import yaml
import platform
import shutil
# from src.utility.utils import copy


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

# config
with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)


# real_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(f"{real_path}")
# sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('.'))
# from src.pdf_parsing.resume_104.pdf_parsing_104 import find_file


# config
# with open("configs/dev_config.yml", "r") as ymlfile:  # FIXME
#     cfg = yaml.load(ymlfile, Loader=yaml.Loader)

# '''共37份檔案測試'''
# data = pd.read_excel(f'.{os.sep}data{os.sep}20231214測試dataframe.xlsx')
# # init_file_path = f'.{os.sep}data{os.sep}test_1214'
# init_file_path = cfg['ALL_CV']['BASE_PATH']
# # output_path= f'.{os.sep}data{os.sep}output{os.sep}20231214'
# output_file_path = cfg['REC_CV']['BASE_PATH']
# files = find_file(base_path=init_file_path, file_extension='pdf')
# names = list()

# '''將所有履歷名字收集'''
# for file in files:
#     names.append(Path(file).stem)


def resume_filter_predict(df, job_class):
    df_filtered = df.loc[
        (df['ans1'] == job_class)
        | (df['ans2'] == job_class)
        ].sort_values(by=['score1', 'score2'], ascending=[True, True])
    # ddf.to_csv(f'{output_path}{os.sep}{job_class}.csv',index=False, encoding='utf-8-sig')
    # df_ans1 = df[df['ans1']== job_class]
    # df_ans1_sorted = df_ans1.sort_values(by='score1')
    # df_ans2 = df[df['ans2']== job_class]
    # df_ans2_sorted = df_ans2.sort_values(by='score2')
    # df_filtered = pd.concat([df_ans1_sorted,df_ans2_sorted])
    return df_filtered


def read_rec_lst(pdf):
    """
    read df[name] from resume_filter_predict
    """

    # pdf = pd.read_csv(f'{output_path}{os.sep}{df_title}.csv')
    lst = list(pdf[cfg['ALL_CV']['FILE_NAMES']])
    return lst


def cp_cv(rec_lst, init_path, output_path, job):
    """
    # FIXME: consider cp cuz if there is no cv, then it is no way to mv again
    :param full_lst:
    :param rec_lst:
    :return:
    """
    # read names
    for idx, resume in enumerate(rec_lst, start=1):
        # copy(from_path=f'{init_path}{os.sep}{resume}.pdf', to_path=f'{output_path}{os.sep}{job}{os.sep}{idx:03}_{resume}.pdf')  # english resume cannot be copied
        shutil.copy(f'{init_path}{os.sep}{resume}.pdf', f'{output_path}{os.sep}{job}{os.sep}{idx:03}_{resume}.pdf')


# job_list = ['保全服務部專案人員','保單行政人員','客服人員','核保人員','理賠審核人員']
# for job in cfg['TITLES']:
#     resume_df = resume_filter_predict(df=data,job_class=job,output_path=output_file_path)
#     lst = read_rec_lst(df_title=resume_df)
#     cp_cv(full_lst=names,
#           rec_lst=lst,
#           init_path=init_file_path,
#           output_path=output_file_path,
#           job=job)
