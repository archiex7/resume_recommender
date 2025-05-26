import glob
import os
import pandas as pd
import numpy as np
from tabulate import tabulate
import pdfplumber
from time import sleep
import re
from tqdm import tqdm_notebook
import cv2 as cv
from pathlib import Path


'''extract job class'''
def find_class(base_path):
    folder = [f.path for f in os.scandir(base_path) if f.is_dir()]
    return folder

'''extract pdf file'''
def find_file(base_path, file_extension):
    return glob.glob(f'{base_path}{os.sep}*.{file_extension}')

'''extract pdf text and concat strings'''
def extract_text(pdf):
    """
    pdfplumber implementation
    :param pdf:
    :return:
    """
    # print(f'pdf: {pdf}')
    pdf_str = ''
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = page.extract_text(x_tolerance=17, y_tolerance=3)  # FIXME: pdfplumber chinese character parsing issue: '⼤學' != '大學'
        pdf_str = pdf_str + text
    # print(f'extract_text: {pdf_str}')
    return pdf_str

# def extract_text(pdf):
#     """
#     pdfminer implementation - for encoding of chinese characters
#     :param pdf:
#     :return:
#     """
#     from pdfminer.layout import LAParams
#     from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#     from pdfminer.converter import TextConverter
#     from pdfminer.pdfpage import PDFPage
#     from io import StringIO
#
#     def extract_text_from_pdf(file_path):
#         resource_manager = PDFResourceManager()
#         fake_file_handle = StringIO()
#         converter = TextConverter(resource_manager, fake_file_handle, codec='big5',
#                                   laparams=LAParams(char_margin=10.0, line_margin=1.5))
#         page_interpreter = PDFPageInterpreter(resource_manager, converter)
#
#         with open(file_path, 'rb') as fh:
#             for page in PDFPage.get_pages(fh,
#                                           caching=True,
#                                           check_extractable=True):
#                 page_interpreter.process_page(page)
#
#             text = fake_file_handle.getvalue()
#
#         # close open handles
#         converter.close()
#         fake_file_handle.close()
#
#         if text:
#             return text
#
#     # file_path = './data/HR_Sherry/test_1214/劉懿賢.pdf'  # replace with your file path
#     file_path = pdf
#     text = extract_text_from_pdf(file_path)
#     print(text)
#     return text


def extract_info(st, patterns):
    dic = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, st, re.DOTALL)
        if match and match.group(1) is not None:
            dic[key] = match.group(1).replace('⾃傳:', '').replace('英文', '')
        elif match and match.group(2) is not None:
            dic[key] = match.group(2).replace('⾃傳:', '').replace('英文', '')
    return dic

def regex(st):
    patterns = {
        '年齡': r"年齡:\s*\d+\((\d+)\)",
        '總年資': r"年資:(.*?)(?=特殊⾝份)",
        'email': r"email:(.*?)(?=聯絡⽅式:)",
        '手機': r"⼿機1:(.*?)(?=⼿機2:)",
        '應徵職務': r"應徵職務(.*?)(?=工作經驗)",
        '工作經驗': r"工作經驗\n(.*?)(?=教育背景)|應徵⼈選 0\n工作經驗(.*?)(?=教育背景)",
        '教育背景': r"教育背景(.*?)(?=求職條件)|學歷資料(.*?)(?=理想職務)",
        '才能專長': r"才能專⻑(.*?)(?=⾃我介紹)",
        '自我介紹': r"⾃我介紹(.*?)(?=#名稱 檔案/連結|$)"
    }
    return extract_info(st, patterns)
