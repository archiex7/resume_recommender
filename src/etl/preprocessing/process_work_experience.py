import logging
import sys
import re
import os
import pdfplumber
import pandas as pd
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.preprocessing.cvtemplate_version import *


def make_perfect(jt, wc):
    '''將工作內容裡的職務名稱去除 & 去除雜訊'''
    for i in range(len(wc)):
        wc[i] = wc[i].strip()
        wc[i] = wc[i].replace('⼯作內容:','')
        wc[i] = re.sub("[上下]午\d+:\d+", '', str(wc[i])) #TODO:篩掉上午下午幾點 姓名
        if wc[i].isalpha(): # 若為英文則不處理
            pass
        else:
            if jt[i] in wc[i]:
                wc[i] = wc[i].replace(jt[i],'')
    return wc

def process_work_experience(con_df):
    cv_template_1 = CvTemplate1()
    cv_template_2 = CvTemplate2()
    cv_template_3 = CvTemplate3()
    job_titles = []
    job_category = []
    work_contents = []
    work_exps = con_df['工作經驗']
    for work_exp in work_exps:
        temp_job_titles = cv_template_1.job_title_parser(input_str=work_exp)['job_titles']
        temp_job_category = cv_template_1.job_category_parser(input_str=work_exp)['job_category']
        temp_work_contents = cv_template_1.work_content_parser(input_str=work_exp)['work_contents']
        length = cv_template_1.job_title_parser(input_str=work_exp)['length']
        if length == 0:
            pass
        else:
            # check which template
            first_item = temp_job_titles[0]
            if ('管理責任' not in first_item) and ('薪資待遇' not in first_item) and ('離職原因' not in first_item):  # template 1
                pass
            elif ('管理責任' not in first_item) and ('薪資待遇' in first_item) and ('離職原因' not in first_item):  # template 2
                temp_job_titles = cv_template_2.job_title_parser(input_str=work_exp)['job_titles']
                temp_job_category = cv_template_2.job_category_parser(input_str=work_exp)['job_category']
                temp_work_contents = cv_template_2.work_content_parser(input_str=work_exp)['work_contents']
                length = cv_template_2.job_title_parser(input_str=work_exp)['length']
            elif ('管理責任' in first_item) and ('薪資待遇' in first_item) and ('離職原因' in first_item):  # template 3
                temp_job_titles = cv_template_3.job_title_parser(input_str=work_exp)['job_titles']
                temp_job_category = cv_template_3.job_category_parser(input_str=work_exp)['job_category']
                temp_work_contents = cv_template_3.work_content_parser(input_str=work_exp)['work_contents']
                length = cv_template_3.job_title_parser(input_str=work_exp)['length']
        temp_work_contents = make_perfect(temp_job_titles, temp_work_contents)
        # fill the list until the certain length
        temp_job_titles = temp_job_titles + [None] * (10 - length)
        temp_job_category = temp_job_category + [None] * (10 - length)
        temp_work_contents = temp_work_contents + [None] * (10 - length)
        # final answer
        job_titles.append(temp_job_titles)
        job_category.append(temp_job_category)
        work_contents.append(temp_work_contents)
    con_df['job_titles'] = job_titles
    con_df[['職務名稱一', '職務名稱二', '職務名稱三', '職務名稱四', '職務名稱五',
        '職務名稱六', '職務名稱七', '職務名稱八', '職務名稱九', '職務名稱十']] = pd.DataFrame(con_df['job_titles'].tolist(), index= con_df.index)
    
    con_df['job_category'] = job_category
    con_df[['職務類別一', '職務類別二', '職務類別三', '職務類別四', '職務類別五',
        '職務類別六', '職務類別七', '職務類別八', '職務類別九', '職務類別十']] = pd.DataFrame(con_df['job_category'].tolist(), index= con_df.index)

    con_df['work_contents'] = work_contents
    con_df[['工作內容一', '工作內容二', '工作內容三', '工作內容四', '工作內容五',
        '工作內容六', '工作內容七', '工作內容八', '工作內容九', '工作內容十']] = pd.DataFrame(con_df['work_contents'].tolist(), index=con_df.index)
    
    return con_df