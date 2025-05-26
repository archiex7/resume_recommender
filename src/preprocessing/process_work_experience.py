import re
import pandas as pd
import logging
import argparse
import warnings
import os
import yaml
from src.utility.utils import Logger
from src.preprocessing.cvtemplate_version import CvTemplate1,CvTemplate2,CvTemplate3

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:  # FIXME: Rain needs to check this in local (win) environment
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
# logger.log(f'config: {cfg}')

def make_perfect(jt, wc):
    '''將工作內容裡的職務名稱去除 & 去除雜訊'''
    for i in range(len(wc)):
        if wc[i]:
            wc[i] = wc[i].strip()
            wc[i] = wc[i].replace('⼯作內容:','')
            wc[i] = re.sub("[上下]午\d+:\d+", '', str(wc[i])) #TODO:篩掉上午下午幾點 姓名
            if wc[i].isalpha(): # 若為英文則不處理
                pass
            else:
                if jt[i] and (jt[i] in wc[i]):  # if i < len(jt) and jt[i] in wc[i]:
                    wc[i] = wc[i].replace(jt[i],'')
    return wc

def process_work_experience(con_df):
    cv_template_1 = CvTemplate1()
    cv_template_2 = CvTemplate2()
    cv_template_3 = CvTemplate3()
    job_titles = []
    job_category = []
    work_contents = []
    work_exps = con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['NAME']]
    for work_exp in work_exps:
        temp_job_titles = cv_template_1.job_title_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']]
        temp_job_category = cv_template_1.job_category_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']]
        temp_work_contents = cv_template_1.work_content_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']]
        length = cv_template_1.job_title_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']]
        if length == 0:
            pass
        else:
            # check which template
            first_item = temp_job_titles[0]
            if ('管理責任' not in first_item) and ('薪資待遇' not in first_item) and ('離職原因' not in first_item):  # template 1
                pass
            elif ('管理責任' not in first_item) and ('薪資待遇' in first_item) and ('離職原因' not in first_item):  # template 2
                temp_job_titles = cv_template_2.job_title_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']]
                temp_job_category = cv_template_2.job_category_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']]
                temp_work_contents = cv_template_2.work_content_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']]
                length = cv_template_2.job_title_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']]
            elif ('管理責任' in first_item) and ('薪資待遇' in first_item) and ('離職原因' in first_item):  # template 3
                temp_job_titles = cv_template_3.job_title_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']]
                temp_job_category = cv_template_3.job_category_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']]
                temp_work_contents = cv_template_3.work_content_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']]
                length = cv_template_3.job_title_parser(input_str=work_exp)[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']]
        # temp_work_contents = make_perfect(temp_job_titles, temp_work_contents)
        # fill the list until the certain length
        temp_job_titles = temp_job_titles + [None] * (10 - length)
        temp_job_titles = temp_job_titles[0:10]  # to ensure there are only 10 elements
        temp_job_category = temp_job_category + [None] * (10 - length)
        temp_job_category = temp_job_category[0:10]  # to ensure there are only 10 elements
        temp_work_contents = temp_work_contents + [None] * (10 - length)
        temp_work_contents = temp_work_contents[0:10]  # to ensure there are only 10 elements
        temp_work_contents = make_perfect(temp_job_titles, temp_work_contents)
        # final answer
        job_titles.append(temp_job_titles)
        job_category.append(temp_job_category)
        work_contents.append(temp_work_contents)
    con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']] = job_titles
    con_df[[col for col in cfg['REC_CV']['INPUT_COLUMNS']['JOB_TITLES']]] = pd.DataFrame(con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']].tolist(), index= con_df.index)
    
    con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']] = job_category
    con_df[[col for col in cfg['REC_CV']['INPUT_COLUMNS']['JOB_CATS']]] = pd.DataFrame(con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']].tolist(), index= con_df.index)

    con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']] = work_contents
    con_df[[col for col in cfg['REC_CV']['INPUT_COLUMNS']['JOB_CONTS']]] = pd.DataFrame(con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']].tolist(), index=con_df.index)
    
    return con_df
