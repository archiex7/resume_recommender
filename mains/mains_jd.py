import logging
import sys
import os
import pdfplumber
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.pdf_parsing.jd.pdf_parsing_jd import *


ddate = '20230922'
# input_base_path = f'.{os.sep}data{os.sep}jd{os.sep}20231005{os.sep}客戶權益部-客訴處理人員_內部徵才工作職能說明_20231003.pdf'
input_base_path = f'.{os.sep}data{os.sep}jd{os.sep}{ddate}'
con_df = pd.DataFrame()
files = find_file(base_path=input_base_path, file_extension='pdf')
for file in files:
    tmp = pdfplumber.open(file)
    table = extract_pdf(page=tmp)
    dic = list_to_dict(table_preprocess(t=table))
    dataF = pd.DataFrame.from_dict(dic, orient='index').T
    con_df = pd.concat([con_df,dataF],ignore_index=True)

# output_path = f'.{os.sep}data{os.sep}output{os.sep}J0713{os.sep}resume_recommender_env{os.sep}resume_recommender_update{os.sep}data{os.sep}data_pdf_parsing{os.sep}jd'
output_path = f'.{os.sep}data{os.sep}output{os.sep}jd'
con_df.to_excel(f'{output_path}{os.sep}jd_concat_{ddate}.xlsx',index=False)