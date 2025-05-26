# -*- coding: utf-8 -*-
import argparse
import sys
import os
import pandas as pd
import datetime
import pytz
import yaml
import warnings
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.preprocessing.cvtemplate_version import *
from src.embedding.five_class_get_two_ans import *
from src.utility.utils import Logger, convert_characters


warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()
logger = Logger(name="main program", log_file=None, log_level=logging.INFO)
# config
with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
logger.log(f'config: {cfg}')

today_date = datetime.datetime.now(tz=pytz.timezone('Asia/Taipei')).strftime('%Y%m%d')
logger.log(f'todayDate: {today_date}')

def to_lower_no_space(string):
    return str(string.lower().replace(" ", ""))

def get_experiences(in_string):
    '''
        preprocess resume content from RPA
    '''
    ans = []
    in_string = str(in_string)
    if in_string and (in_string != 'nan'):
        pattern1 = r'\d{4}/\d{2}/\d{2} ~ \d{4}/\d{2}/\d{2}'
        pattern2 = r'\d{4}/\d{2}/\d{2} ~ 仍在職'
        split_string = re.split(pattern1 + '|' + pattern2, in_string)
        ans = [to_lower_no_space(string.strip().split('\n')[-1]) for string in split_string if string]
    return ans

# read abbreviated resumes parsed by RPA
df = pd.read_csv(f"{cfg['ITHR']['BASE_PATH']}{os.sep}{today_date}{os.sep}{cfg['ITHR']['STAGE_1']}{os.sep}{cfg['ITHR']['CV']['FILE_NAME']}", encoding="utf-8-sig")
logger.log(f'{len(df)} 104-ids and abbreviated resumes are crawled by RPA.')
df[[f"{cfg['ITHR']['CV']['NAME']}", f"{cfg['ITHR']['CV']['ID']}"]] = df[f"{cfg['ITHR']['CV']['NAME_ID']}"].str.split('\n', expand=True)
df[f"{cfg['ITHR']['CV']['ID']}"] = df[f"{cfg['ITHR']['CV']['ID']}"].astype(str)
df[f"{cfg['ITHR']['CV']['WORK_EXPS']}"] = df.apply(lambda row: get_experiences(row[f"{cfg['ITHR']['CV']['WORK_EXP']}"]), axis=1)

# read non-duplicated list
df_non_dup_lst = pd.read_csv(f"{cfg['ITHR']['BASE_PATH']}{os.sep}{cfg['ITHR']['NON_DUP_LST']['FILE_NAME']}", encoding="utf-8-sig")
df_non_dup_lst[f"{cfg['ITHR']['CV']['ID']}"] = df_non_dup_lst[f"{cfg['ITHR']['CV']['ID']}"].astype(str)  # type casting for 104ID
# print(f"type(df_non_dup_lst id): {type(df_non_dup_lst[cfg['ITHR']['CV']['ID']][0])}")
# print(f"type(df id): {type(df[cfg['ITHR']['CV']['ID']][0])}")
# list comparison
# TODO
df = df.loc[~df[cfg['ITHR']['CV']['ID']].isin(df_non_dup_lst[cfg['ITHR']['CV']['ID']])]
logger.log(f"{len(df)} 104-ids are left after eliminating those on the non-duplicated list.")

# read titles
df_cond = pd.read_excel(
    f"{cfg['ITHR']['BASE_PATH']}{os.sep}{cfg['ITHR']['TITLES']['FILE_NAME']}",
    sheet_name=f"{cfg['ITHR']['TITLES']['SHEET_NAME']}",
    header=None,
)
df_cond[0] = df_cond.apply(lambda row: to_lower_no_space(row[0]), axis=1)
occupations = set(df_cond[0])
# check whether in occupations
lst = list()
df['status'] = 'unmatch'
for elem in df.to_dict('records'):
    exp = elem[f"{cfg['ITHR']['CV']['WORK_EXPS']}"]
    if exp:
        for job in exp:
            if job in occupations:
                elem['status'] = f'{job}'
                lst.append(elem)
                break
logger.log(f"{len(lst)} 104-ids are left after filtering matched titles.")
# set upper limit
lst = lst[0:int(f"{cfg['ITHR']['OUTPUT_IDS']['NUM_LIMIT']}")]
logger.log(f"{len(lst)} 104-ids are left, RPA should crawl these data in stage_2. (Upper limit is set to: {cfg['ITHR']['OUTPUT_IDS']['NUM_LIMIT']})")

# select columns and then output as a file
if lst:
    df_output = pd.DataFrame(lst)[[f"{cfg['ITHR']['CV']['NAME']}", f"{cfg['ITHR']['CV']['ID']}"]]
else:
    df_output = pd.DataFrame({f"{cfg['ITHR']['CV']['NAME']}": [], f"{cfg['ITHR']['CV']['ID']}": []})
logger.log(f'Outputting the id list for RPA to download files, shape of df_output: {df_output.shape[0]}.')
df_output.to_excel(f"{cfg['ITHR']['BASE_PATH']}{os.sep}{today_date}{os.sep}{cfg['ITHR']['STAGE_2']}{os.sep}{cfg['ITHR']['OUTPUT_IDS']['FILE_NAME']}", sheet_name=f"{cfg['ITHR']['TITLES']['SHEET_NAME']}")
logger.log(f'ITHR stage 1 done successfully.')

# df_unmatch = df.loc[df['status'] == 'unmatch', [cfg['ITHR']['CV']['NAME'], cfg['ITHR']['CV']['WORK_EXPS'], 'status']]
# logger.log(f'''
# logger - DEBUG - df_unmatch: check the status filtered by titles
# shape of dataframe: {df_unmatch.shape}
# head: {df_unmatch.head(5)}
# tail: {df_unmatch.tail(5)}
# ''')
