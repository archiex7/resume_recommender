# -*- coding: utf-8 -*-
import pandas as pd
import yaml
import os
import sys
from pathlib import Path
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.etl.pdf_parsing.pdf_parsing_104 import find_file


# config
with open("configs/dev_config.yml", "r") as ymlfile:  # FIXME
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)


# FIXME: hard code
# read all pdf files in one specific dir
all_cv_base_path = f'.{os.sep}data{os.sep}test_1214'  # cfg['ALL_CV']['BASE_PATH']
files = find_file(base_path=all_cv_base_path, file_extension='pdf')
# 共37份檔案測試
data = pd.read_excel(f'.{os.sep}data{os.sep}20231214測試dataframe.xlsx')
output_path = f'.{os.sep}data{os.sep}output{os.sep}20231214'
names = list()
# 將所有履歷名字收集
for file in files:
    names.append(Path(file).stem)


# def read_rec_lst(base_path, job_title):
#     """
#     read names from each job title
#     """
#     # base_path = path
#     # file_name = file_name
#     pdf = pd.read_csv(f'{base_path}{os.sep}{job_title}.csv')
#     lst = set(pdf['姓名'])  # FIXME
#     return lst


def read_rec_lst(pdf):
    """
    read df[name] from resume_filter_predict
    """
    # pdf = pd.read_csv(f'{output_path}{os.sep}{df_title}.csv')
    lst = set(pdf['姓名'])  # FIXME
    return lst


def cp_cv(full_lst, f_base_path, rec_lst, r_base_path, job):
    # read names
    for name in full_lst:
        if name in rec_lst:
            os.system(f'copy {f_base_path}{os.sep}{name}.pdf {r_base_path}{os.sep}{job}')


# rec_base_path = cfg['REC_CV']['BASE_PATH']
# for title in cfg['TITLES']:
#     rec_list = read_rec_lst(base_path=rec_base_path, job_title=title)
#     cp_cv(full_lst=names, f_base_path=all_cv_base_path, rec_lst=rec_list, r_base_path=rec_base_path)


def resume_filter_predict(df, job_class, output_path):
    ddf = df.loc[
        (df['ans1'] == job_class)
        | (df['ans2'] == job_class)
    ].sort_values(by=['score1', 'score2'], ascending=[True, True])
    ddf.to_csv(f'{output_path}{os.sep}{job_class}.csv', index=False, encoding='utf-8-sig')
    return ddf


for title in cfg['TITLES']:
    resume_df = resume_filter_predict(df=data, job_class=title, output_path=output_path)
    lst = read_rec_lst(pdf=resume_df)
    cp_cv(
        full_lst=names,
        f_base_path=all_cv_base_path,
        rec_lst=lst,
        r_base_path=output_path,
        job=title
    )
