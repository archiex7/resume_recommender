# -*- coding: utf-8 -*-
import argparse
from datetime import datetime, timedelta
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import logging
import os
import pandas as pd
from pathlib import Path
import pdfplumber
import sys
import time
import warnings
import yaml
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.pdf_parsing.resume_104.pdf_parsing_104 import find_file, extract_text, regex
from src.preprocessing.preprocess_insurance import regex_sub
from src.preprocessing.process_work_experience import process_work_experience
from src.preprocessing.process_educational_background import process_educational_background
from src.preprocessing.process_seniority import process_seniority
from src.embedding.five_class_get_two_ans import concat_str, filter_freshman, pdf_to_other, get_similarity_positions
from src.rule.prediction_filter import resume_filter_predict, read_rec_lst, cp_cv
from src.mail.send_file import send_outlook_email
# from src.mail.send_file_windows_version import send_outlook_email
# from src.mail.send_file_linux_version import send_email
from src.utility.utils import Logger, convert_characters, get_file_name, get_104_id


warnings.filterwarnings("ignore")
# argument
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()
# log
logger = Logger(name="main program", log_file=None, log_level=logging.INFO)
# config
with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
logger.log(f'config: {cfg}')

today = datetime.today().date()
todayDate = today.strftime('%Y%m%d')
logger.log(f'todayDate: {todayDate}')
init_path = f"{cfg['ITHR']['BASE_PATH']}{os.sep}{todayDate}{os.sep}{cfg['ALL_CV']['SUB_DIR']}"
output_path = f"{cfg['ITHR']['BASE_PATH']}{os.sep}{todayDate}{os.sep}{cfg['REC_CV']['SUB_DIR']}"
# jd
jd_loader = CSVLoader(
    file_path=f"{cfg['ITHR']['BASE_PATH']}{os.sep}{cfg['JD']['FILE_NAME']}",
    source_column="職缺名稱", encoding="UTF-8"
)
jd_docs = jd_loader.load()
# embedding model for text vectorization
embedding_model = HuggingFaceEmbeddings(model_name=cfg['EMD_MODEL']['BASE_PATH'],
                                        encode_kwargs={'normalize_embeddings': True}, model_kwargs={'device': f'{cfg["DEVICE"]}'})
# vector store
jd_docs_knowledge_base = FAISS.from_documents(jd_docs, embedding_model)
file_names = list()
names = list()
id_104 = list()
con_df = pd.DataFrame()
# print(f'model loaded: {embedding_model}')

if not os.path.exists(output_path):
    os.makedirs(output_path)
job_list = [title for title in cfg['TITLES']]  # [doc.metadata['source'] for doc in jd_docs]  # read from csvloader
for title in job_list:
    if not os.path.exists(f"{output_path}{os.sep}{title}"):
        os.makedirs(f"{output_path}{os.sep}{title}")

files = find_file(base_path=init_path, file_extension='pdf')
for file in files:
    file_names.append(Path(file).stem)
    names.append(get_file_name(Path(file).stem))
    id_104.append(get_104_id(Path(file).stem))
logger.log(f'''total files: {len(file_names)}, first 5 file_names: {file_names[0:4]}''')

'''pdf_parsing'''  # extract data in a bigger scope
logger.log(f'''Start parsing texts from pdf files...''')
for file in files:
    dic_all = regex(convert_characters(extract_text(pdfplumber.open(file))))
    dataF = pd.DataFrame.from_dict(dic_all, orient='index').T
    con_df = pd.concat([con_df, dataF], ignore_index=True)
con_df[cfg['ALL_CV']['FILE_NAMES']] = file_names
con_df[cfg['ITHR']['CV']['NAME']] = names
con_df[cfg['ITHR']['CV']['ID']] = id_104
# con_df.to_excel(f'{output_path}{os.sep}test_ori.xlsx', index=False)
# con_df.to_csv(f'{output_path}{os.sep}{todayDate}_name.csv', index=False, encoding='utf-8-sig')  # TODO: for debug - check encoding issue - UnicodeEncodeError: 'cp950' codec can't encode character '\u2fbc'
logger.log(f'''Done successfully - pdf_parsing, shape of dataframe: {con_df.shape}''')

'''preprocess'''  # extract more detailed data from each column
for feat in con_df.columns:
    con_df[feat] = regex_sub(df=con_df[feat])
con_df = process_seniority(con_df=con_df)
con_df = process_work_experience(con_df=con_df)
con_df = process_educational_background(con_df=con_df)
# con_df = process_highest_education(con_df=con_df)
# con_df.to_csv(f'{output_path}{os.sep}{todayDate}_preprocess.csv', index=False, encoding='utf-8-sig')
con_df = concat_str(df=con_df)
logger.log(f'Done successfully - preprocess, shape of dataframe: {con_df.shape}')

'''filter freshman to folder others'''
con_df, other_df = filter_freshman(df=con_df)
pdf_to_other(df=other_df,
             init_path=init_path,
             output_path=output_path)
logger.log(f'Done successfully - copied empty CVs to "others" directory')

'''embedding'''
con_df['answer'], con_df['score'] = zip(*con_df.apply(
    lambda row: get_similarity_positions(jd_docs_knowledge_base, row=row['resume_string'], num=2), axis=1))

con_df[['ans1', 'ans2']] = pd.DataFrame(con_df['answer'].to_list(), index=con_df.index)
con_df[['score1', 'score2']] = pd.DataFrame(con_df['score'].to_list(), index=con_df.index)
logger.log(f'Done successfully - embedding, now we get recommended answers and similarity scores')
# columns Roger wants to add
con_df[[col for col in cfg["REC_CV"]["ADD_COLUMNS"]]] = ''

# '''post process - hr rules - annotation'''
# empty

# output master table
con_df[[col for col in cfg["REC_CV"]["OUTPUT_COLUMNS"]]].to_csv(f'{output_path}{os.sep}{todayDate}_emb.csv', index=False, encoding="utf-8-sig")
logger.log(f'''Done successfully - output all result: emb.csv
shape of dataframe: {con_df.shape}
head: {con_df.head(3)}''')
# logger.log(f'con_df.columns - {con_df.columns}')
# logger.log(f'con_df.loc[0].to_dict() - {con_df.loc[0].to_dict()}')

'''prediction filter'''
for job in job_list:
    resume_df = resume_filter_predict(df=con_df, job_class=job)
    # output each table
    resume_df[[col for col in cfg["REC_CV"]["OUTPUT_COLUMNS"]]].to_csv(f'{output_path}{os.sep}{job}{os.sep}{job}.csv', index=False, encoding='utf-8-sig')
    lst = read_rec_lst(pdf=resume_df)
    cp_cv(rec_lst=lst, init_path=init_path, output_path=output_path, job=job)
logger.log(f'Done successfully - copied CVs from base path: "{init_path}" to path: "{output_path}"')

'''send mail'''
time.sleep(3)
# FIXME
send_outlook_email(subject=f"{todayDate}模型執行確認信件",
                   body = "已成功完成執行，附件為履歷分類結果",
                   to = f"{cfg['EMAIL']['MAINTAINER']}",
                   attachment_path = f'{output_path}{os.sep}{todayDate}_emb.csv',
                   sender = f"{cfg['EMAIL']['SENDER']}")

logger.log(f'Done successfully - email is sent to maintainers with an attachment {todayDate}_emb.csv')


'''non_duplicated_lst'''
date_lst = list()
end_date = datetime.now().strftime('%Y%m%d')
# get the date list from today to past 30 days
start_date = (datetime.now() - timedelta(days=int(f"{cfg['ITHR']['NON_DUP_LST']['DATE_RANGE']}"))).strftime('%Y%m%d')
all_data = pd.DataFrame()

for date_str in pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y%m%d'):
    date_lst.append(date_str)
    folder_path = os.path.join(f"{cfg['ITHR']['BASE_PATH']}", date_str, f"{cfg['REC_CV']['SUB_DIR']}")
    if os.path.exists(folder_path):
        csv_file = os.path.join(folder_path, f'{date_str}_emb.csv')
        if os.path.exists(csv_file):
            data = pd.read_csv(csv_file, encoding='utf-8')
            data[cfg['ITHR']['NON_DUP_LST']['DATE']] = date_str
            data = data[cfg['ITHR']['NON_DUP_LST']['OUTPUT_COLUMNS']]
            all_data = pd.concat([all_data, data], ignore_index=True)

all_data.to_csv(os.path.join(f"{cfg['ITHR']['BASE_PATH']}", 'non_duplicated_lst.csv'), index=False, encoding='utf-8-sig')
logger.log(f'''Done successfully - output: non_duplicated_lst.csv
shape of dataframe: {all_data.shape}
head: {all_data.head(2)}
tail: {all_data.tail(2)}
date_lst begins from: "{date_lst[0]}" to: "{date_lst[-1]}"''')

''' notify managers to check the result'''
send_outlook_email(subject=f"IT招募公務信箱提醒您至WIKI審閱履歷_{todayDate}",
                   body = r"""部長好,
今日履歷備妥，提醒您至WIKI下載、審閱履歷，並記錄您的書審結果。
\\sptwfap00086\\DATA\\IT_Resume
謝謝
""",
                   to = f"{cfg['EMAIL']['MANAGER']}",
                   sender = f"{cfg['EMAIL']['SENDER']}")
logger.log(f'Done successfully - email is sent to manaers.')

logger.log(f'All tasks are done successfully in stage 2.')
