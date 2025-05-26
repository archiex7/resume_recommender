import glob
import os
import pandas as pd
import numpy as np
from tabulate import tabulate
import pdfplumber
import re

def find_file(base_path, file_extension):
    return glob.glob(f'{base_path}{os.sep}*.{file_extension}')

def extract_pdf(page):
    if len(page.pages) == 1:   
        pages = page.pages[0]           
        tables = pages.extract_table()
    return tables

def update_position(li):
    position = li[3]
    if position != '□管理職█非管理職' and position != '█管理職□非管理職':
        pass
    elif position == '□管理職█非管理職':
        li[3] = '非管理職'
    else:
        li[3] = '管理職'
    return li

def language_proficiency(str):
    pattern = r"英文:.*■(\w+).*其他:.*■(\w+)"
    match = re.search(pattern, str)
    if match:
        output = "英文:{};其他:{}".format(match.group(1), match.group(2))
    elif re.search(r"英文:.*■(\w+).*其他:", str):
        output = "英文:{}".format(re.search(r'英文:.*■(\w+).*其他:', str).group(1))
    elif re.search(r"英文:.*其他:.*■(\w+)", str):
        output = "其他:{}".format(re.search(r'英文:.*其他:.*■(\w+)', str).group(1))
    elif re.search(r"英文:.*■(\w+)",str):
        output = "英文:{}".format(re.search(r'英文:.*■(\w+)', str).group(1))
    elif re.search(r"其他:.*■(\w+)",str):
        output = "其他:{}".format(re.search(r'其他:.*■(\w+)', str).group(1))
    else:
        output = "無"
    return output

def table_preprocess(t):
    updated_table = []  
    for row in t:
        updated_row = [cell for cell in row if cell]  # 去除None
        updated_row = [cell.replace(" ", "") for cell in updated_row]  # 去空格
        updated_row = [cell.replace("\n", "") for cell in updated_row] # 去換行
        updated_table.append(updated_row)

    for row in updated_table:
        if len(row)== 4:
            update_position(row)
    return updated_table

def list_to_dict(list_of_lists):
    complete_dict = {}
    for ele in list_of_lists:
        if len(ele) == 1:
            continue
        elif len(ele) == 2:
            if '□' in ele[1]:
                ele[1] = language_proficiency(ele[1])
                dic = {ele[0]:ele[1]}
                complete_dict.update(dic)
            else:
                dic = {ele[0]:ele[1]}
                complete_dict.update(dic)
        elif len(ele) == 3:
            if ele[0] == '職務聯絡人':
                dic = {ele[0]:ele[1]+' '+ele[2]}
                complete_dict.update(dic)
            else:
                dic = {ele[1]:ele[2]}
                complete_dict.update(dic)
        elif len(ele) == 4:
            dic = {ele[0]:ele[1]}
            dic1 = {ele[2]:ele[3]}
            complete_dict.update(dic)
            complete_dict.update(dic1)
    return complete_dict