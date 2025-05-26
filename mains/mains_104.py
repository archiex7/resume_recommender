import logging
import sys
import os
import pdfplumber
import pandas as pd
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.pdf_parsing.resume_104.pdf_parsing_104 import *
from src.preprocessing.preprocess_insurance import *
from src.preprocessing.cvtemplate_version import *
from src.preprocessing.process_work_experience import *
from src.preprocessing.process_educational_background import *
from src.preprocessing.process_seniority import *
from src.embedding.five_class_get_two_ans import *
from src.embedding.find_best_fit import *


init_path = f'.{os.sep}data{os.sep}104_resume{os.sep}Sherry'
init_path = f'.{os.sep}data{os.sep}test_1124'
class_files = find_class(base_path=init_path)
for class_file in class_files:
    con_df = pd.DataFrame()
    name = []
    class_name = Path(class_file).stem
    files = find_file(base_path=class_file, file_extension='pdf')
    for file in files:
        name.append(Path(file).stem)
        dic_all = regex(extract_text(pdfplumber.open(file)))
        dataF = pd.DataFrame.from_dict(dic_all, orient='index').T
        con_df = pd.concat([con_df,dataF],ignore_index=True)
        con_df['姓名'] = name
        con_df['label'] = class_name
    
    ## modify
    output_path = f'.{os.sep}data{os.sep}output{os.sep}pipeline_test_1129'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # con_df.to_excel(f'{output_path}{os.sep}pdf_parsing_{class_name}.xlsx',index=False)

# preprocess
    for feat in con_df.columns:
        con_df[feat] = regex_sub(df=con_df[feat])

    con_df = process_seniority(con_df=con_df)
    con_df = process_work_experience(con_df=con_df)
    con_df = process_educational_background(con_df=con_df)
    con_df.to_excel(f'{output_path}{os.sep}{class_name}.xlsx',index=False)

# embedding
emb_df = pd.DataFrame()
resumes = find_excel_file(base_path=output_path, file_extension='xlsx')
for res in resumes:
    tmp = pd.read_excel(res)
    resume = pd.DataFrame(tmp)
    emb_df = pd.concat([emb_df,resume],ignore_index=True)
emb_df = concat_str(df=emb_df)
start = time.time()

loader = CSVLoader(file_path="C:/Users/J0713/Desktop/resume_recommender_project/data/保單行政/104同業生成_1129.csv", source_column="職缺名稱",encoding="UTF-8") # encoding = "UTF-8"
criteria = loader.load()
embeddings = HuggingFaceEmbeddings(model_name="C:/Users/J0713/Desktop/resume_recommender_project/model/tao-8k",encode_kwargs = {'normalize_embeddings': True},model_kwargs={'device':'cpu'})
criteria_knowledge_base = FAISS.from_documents(criteria, embeddings)
emb_df['answer'] = emb_df.apply(lambda row: similarity_position_chunk(criteria_knowledge_base,row=row['resume_string'],num=2), axis=1)
emb_df['score'] = emb_df.apply(lambda row: similarity_position_chunk_score(criteria_knowledge_base,row=row['resume_string'],num=2), axis=1)
end  = time.time()
print(f"elapsed time:{end - start}(s)")
emb_df[['ans1', 'ans2']] = pd.DataFrame(emb_df['answer'].to_list(), index=emb_df.index)
emb_df[['score1','score2']] = pd.DataFrame(emb_df['score'].to_list(), index=emb_df.index)
result = emb_df[['姓名','label','ans1','ans2','score1','score2']]
result.to_excel(f'{output_path}{os.sep}result.xlsx',index=False)

# find best score for each class
labels = ['保全服務部專案人員', '保單行政人員', '客服人員', '核保人員', '理賠審核人員']
results = {}
for label in labels:
    results[label] = find_optimized(ss=(result['label']==label), df=result)

for label, df in results.items():
    df.to_csv(f"{output_path}{os.sep}{label}.csv", index=False, encoding = 'utf-8-sig')
