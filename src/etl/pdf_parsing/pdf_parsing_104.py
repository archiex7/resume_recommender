import glob
import os
import pandas as pd
import numpy as np
from tabulate import tabulate
import pdfplumber
from time import sleep
import re
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import cv2 as cv
from pathlib import Path


#extract class
def find_class(base_path):
    folder = [f.path for f in os.scandir(base_path) if f.is_dir()]
    return folder

#extract data
def find_file(base_path, file_extension):
    return glob.glob(f'{base_path}{os.sep}*.{file_extension}')

#連接所有字串
def extract_text(pdf):
    pdf_str = ''
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = page.extract_text(x_tolerance=17 , y_tolerance=3)
        pdf_str = pdf_str + text
    return pdf_str

def regex(st):
    dic = {}
    # age = r"年齡:(.*?)(?=國籍)"
    age = r"年齡:\((\d+)\)(?=國籍)"
    # age_f = r"(\d{4} \(\d+\))"
    age_f = r"\((\d+)\)"
    # age_m = r"/(.*?)(?=男)"
    total_year = r"年資:(.*?)(?=特殊⾝份)"
    pattern = r"⾃我介紹(.*?)(?=#名稱 檔案/連結|$)"
    pattern1 = r"才能專⻑(.*?)(?=⾃我介紹)"
    pattern2 = r"應徵⼈選 0\n⼯作經驗(.*?)(?=教育背景)"
    pat2 = r"⼯作經驗\n(.*?)(?=教育背景)"
    pattern5 = r"應徵職務(.*?)(?=⼯作經驗)"
    education_background = r"教育背景(.*?)(?=求職條件)"
    education_background1 = r"學歷資料(.*?)(?=理想職務)"
    email = r"email:(.*?)(?=聯絡⽅式:)"
    phone = r"⼿機1:(.*?)(?=⼿機2:)"

    age_match = re.search(age, st, re.DOTALL)
    age_match_f = re.search(age_f, st, re.DOTALL)
    total_year_match = re.search(total_year, st, re.DOTALL)
    # age_match_m = re.search(age_m, st, re.DOTALL)
    email_match = re.search(email, st, re.DOTALL)
    phone_match = re.search(phone, st, re.DOTALL)
    edu_match = re.search(education_background, st, re.DOTALL)
    edu_match1 = re.search(education_background1, st, re.DOTALL)
    match = re.search(pattern, st, re.DOTALL)
    match1 = re.search(pattern1, st, re.DOTALL)
    match2 = re.search(pattern2, st, re.DOTALL)
    mat2 = re.search(pat2, st, re.DOTALL)
    match5 = re.search(pattern5, st, re.DOTALL)
# match4 = re.findall(r'⼯作內容:(.*?)⼯作技能:(.*?)$', text, re.DOTALL)
    if age_match:
        na = {'年齡': age_match.group(1)}
        dic.update(na)
    elif age_match_f:
        amf = {'年齡': age_match_f.group(1)}
        dic.update(amf)
    # else:
    #     amm = {'年齡': age_match_m.group(1)}
    #     dic.update(amm)
    if total_year_match:
        tym = {'總年資':total_year_match.group(1)}
        dic.update(tym)
    if email_match:
        em = {'email':email_match.group(1)}
        dic.update(em)
    if phone_match:
        pm = {'手機':phone_match.group(1)}
        dic.update(pm)
    if match5: 
        ma5 = {'應徵職務':match5.group(1)}
        # dic.update({'應徵職務':match5.group(1)})
        dic.update(ma5)
    if match2: 
        ma2 = {'工作經驗':match2.group(1)}
        dic.update(ma2)
    elif mat2:
        # mat2.group(1).split('工作經驗')
        m = {'工作經驗':mat2.group(1)}
        dic.update(m)
    if edu_match:
        edu = {'教育背景':edu_match.group(1)}
        dic.update(edu)
    elif edu_match1:
        em = {'教育背景':edu_match1.group(1)}
        dic.update(em)
    if match1: 
        ma1 = {'才能專長':match1.group(1)}
        dic.update(ma1)

    if match: 
        ma = {'自我介紹':match.group(1).replace('⾃傳:','').replace('英文','')}
        dic.update(ma)

    return dic