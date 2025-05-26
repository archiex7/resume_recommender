# -*- coding: utf-8 -*-
import logging
import argparse
import warnings
import sys
import os
import pdfplumber
import pandas as pd
import datetime
import yaml
import time
from pathlib import Path
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.pdf_parsing.resume_104.pdf_parsing_104 import find_file, extract_text, regex
from src.preprocessing.preprocess_insurance import regex_sub
from src.preprocessing.process_work_experience import process_work_experience
from src.preprocessing.process_educational_background import process_educational_background
from src.preprocessing.process_seniority import process_seniority
from src.preprocessing.process_highest_education  import process_highest_education
from src.embedding.five_class_get_two_ans import concat_str,filter_freshman, pdf_to_other, get_similarity_positions
from src.rule.prediction_filter import resume_filter_predict, read_rec_lst, cp_cv
# from src.mail.send_file import send_outlook_email
# from src.mail.send_file_windows_version import send_outlook_email
# from src.mail.send_file_linux_version import send_email
from src.utility.utils import Logger, convert_characters
from src.postprocess.hr_rule import Age, Education


warnings.filterwarnings("ignore")


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

# config
with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
logger.log(f'config: {cfg}')

today = datetime.date.today()
todayDate = today.strftime('%Y%m%d')
logger.log(f'todayDate: {todayDate}')
# init_path = f'.{os.sep}data{os.sep}test_1214'
# output_path = f".{os.sep}data{os.sep}output{os.sep}{todayDate}"
init_path = f"{cfg['ALL_CV']['BASE_PATH']}{os.sep}test_1214"
output_path = f"{cfg['REC_CV']['BASE_PATH']}{os.sep}{todayDate}"
loader = CSVLoader(file_path=f"{cfg['ALL_CV']['BASE_PATH']}{os.sep}保單行政{os.sep}104同業生成_1129.csv",
                   source_column="職缺名稱", encoding="UTF-8")
# loader = CSVLoader(file_path="C:/Users/J0713/Desktop/resume_recommender_project/data/保單行政/104同業生成_1129.csv", source_column="職缺名稱",encoding="UTF-8")
jd_docs = loader.load()
# embeddings = HuggingFaceEmbeddings(model_name=cfg['EMD_MODEL']['BASE_PATH'], encode_kwargs = {'normalize_embeddings': True},model_kwargs={'device':'cpu'})
embedding_model = HuggingFaceEmbeddings(model_name=cfg['EMD_MODEL']['BASE_PATH'],
                                        encode_kwargs={'normalize_embeddings': True}, model_kwargs={'device': f'{cfg["DEVICE"]}'})
# embedding_model = HuggingFaceEmbeddings(model_name= "C:/Users/J0713/Desktop/resume_recommender_project/model/tao-8k", encode_kwargs = {'normalize_embeddings': True},model_kwargs={'device':'cpu'})
jd_docs_knowledge_base = FAISS.from_documents(jd_docs, embedding_model)
names = list()
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
    names.append(Path(file).stem)

'''pdf_parsing'''  # extract data in a bigger scope
for file in files:
    dic_all = regex(convert_characters(extract_text(pdfplumber.open(file))))
    dataF = pd.DataFrame.from_dict(dic_all, orient='index').T
    con_df = pd.concat([con_df, dataF], ignore_index=True)
con_df['name'] = names
# con_df.to_excel(f'{output_path}{os.sep}test_ori.xlsx',index=False)
logger.log(f'''Done successfully - pdf_parsing, shape of dataframe: {con_df.shape}''')

'''preprocess'''  # extract more detailed data from each column
for feat in con_df.columns:
    con_df[feat] = regex_sub(df=con_df[feat])
con_df = process_seniority(con_df=con_df)
con_df = process_work_experience(con_df=con_df)
con_df = process_educational_background(con_df=con_df)
con_df = process_highest_education(con_df=con_df)
con_df.to_csv(f'{output_path}{os.sep}{todayDate}_preprocess.csv', index=False, encoding='utf-8-sig')
con_df = concat_str(df=con_df)
logger.log(f'Done successfully - preprocess, shape of dataframe: {con_df.shape}')

'''將履歷小白先分到其他類'''
con_df, other_df = filter_freshman(df=con_df)
pdf_to_other(df=other_df,
             init_path=init_path,
             output_path=output_path)
logger.log(f'Done successfully - empty CVs to "others" directory')

'''embedding'''
con_df['note'] = ""
con_df['answer'], con_df['score'] = zip(*con_df.apply(
    lambda row: get_similarity_positions(jd_docs_knowledge_base, row=row['resume_string'], num=2), axis=1))

con_df[['ans1', 'ans2']] = pd.DataFrame(con_df['answer'].to_list(), index=con_df.index)
con_df[['score1', 'score2']] = pd.DataFrame(con_df['score'].to_list(), index=con_df.index)
logger.log(f'Done successfully - embedding, now we get recommended answers and similarity scores')
# con_df[[col for col in cfg["REC_CV"]["OUTPUT_COLUMNS"]]].to_csv(f'{output_path}{os.sep}{todayDate}_emb.csv', index=False, encoding="utf-8-sig")
# logger.log(f'Done successfully - output all result: emb.csv')

'''post process - hr rules - annotation'''
# init helpers
age_annotator = Age()
edu_annotator = Education()
# logger.log(f'{con_df.loc[0,:]}')
# type casting
con_df['年齡'] = con_df['年齡'].astype(int)
# con_df.info()
# logger.log(con_df[['name', '學校', '科系', '學位', '年齡']].head())
# print(f'{list(con_df["年齡"])}, {len(list(con_df["年齡"]))}')
# TODO: post process - need new columns like 'age'
for job in job_list:
    con_df = age_annotator.annotate(pdf=con_df, position=job)
    con_df = edu_annotator.annotate(pdf=con_df, position=job)  # FIXME
# output master table
con_df[[col for col in cfg["REC_CV"]["OUTPUT_COLUMNS"]]].to_csv(f'{output_path}{os.sep}{todayDate}_emb.csv', index=False, encoding="utf-8-sig")
logger.log(f'Done successfully - output all result: emb.csv')
# logger.log(f'con_df.columns - {con_df.columns}')
# logger.log(f'con_df.loc[0].to_dict() - {con_df.loc[0].to_dict()}')

'''prediction filter'''
for job in job_list:
    resume_df = resume_filter_predict(df=con_df, job_class=job)
    # output each table
    resume_df[[col for col in cfg["REC_CV"]["OUTPUT_COLUMNS"]]].to_csv(f'{output_path}{os.sep}{job}{os.sep}{job}.csv', index=False, encoding='utf-8-sig')
    lst = read_rec_lst(df_title=resume_df)
    cp_cv(rec_lst=lst, init_path=init_path, output_path=output_path, job=job)

'''send mail'''
time.sleep(3)
# FIXME
# send_outlook_email(subject=f"{todayDate}模型執行確認信件",
#                    body = "已成功完成執行",
#                    to = "johnson.sh.huang@fubon.com;haohsuan.hsu@fubon.com",
#                    attachment_path = all_embedding_result,
#                    sender = "rain.yeh@fubon.com")
