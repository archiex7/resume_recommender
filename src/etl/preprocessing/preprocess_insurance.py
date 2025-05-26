import pandas as pd
import numpy as np 
import re
import os
import glob


def regex_sub(df):
    for t in range(len(df)):
        df[t] = re.sub('https?://[^ ]+|[\d/]+ [上下]午\d+:\d+', '',str(df[t]))
        df[t] = re.sub('https?://[^ ]+|[\d/]+ 晚上\d+:\d+', '',str(df[t]))
        df[t] = re.sub(r'專案成就(.*?)(?=。)','',str(df[t]))
        df[t] = str(df[t]).replace('\n', ' ').replace('*','').replace('附件','')
    return df


# def numToCharater(word:str):
#     dic = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': ''}
#     length = len(word)
#     if length == 1:
#         return dic[word[0]]


# def column_process(df):
#     for x in range(len(df['工作經驗'])):
#         input_string = df['工作經驗'][x]
#         if type(input_string) != str:
#             continue
#         else:
#             seniority = r"\((\d+ ?年 ?\d+ ?個 ?⽉)\)"
#             title = r"職務名稱:(.*?)(?=薪資待遇)"
#             title1 = r"職務名稱:(.*?)(?=管理責任)"
#             content = r"薪資待遇:(.*?)(?=⼯作技能)"
#             content1 = r"職務名稱:(.*?)(?=⼯作技能)"
#             seniority_match = re.findall(seniority, input_string)
#             title_match = re.findall(title, input_string, re.DOTALL)
#             title1_match = re.findall(title1, input_string, re.DOTALL)
#             content_match = re.findall(content, input_string, re.DOTALL)
#             content1_match = re.findall(content1, input_string, re.DOTALL)
            
#             if seniority_match:
#                 for id,du in enumerate(seniority_match):
#                     df.loc[x,f'工作經驗{numToCharater(str(id+1))}年資'] = du
#             if title1_match:
#                 for idx,d in enumerate(title1_match):
#                     df.loc[x,f'職務名稱{numToCharater(str(idx+1))}'] = d
#             elif title_match: 
#                 for idx,d in enumerate(title_match):
#                     df.loc[x,f'職務名稱{numToCharater(str(idx+1))}'] = d
#             if content_match:
#                 for i,a in enumerate(content_match):
#                     a = a.replace('⼯作內容:','')
#                     df.loc[x,f'工作內容{numToCharater(str(i+1))}'] = a
#             elif content1_match:
#                 for i,a in enumerate(content1_match):
#                     a = a.replace('⼯作內容:','')
#                     df.loc[x,f'工作內容{numToCharater(str(i+1))}'] = a

#         input_string1 = df['教育背景'][x]
#         if type(input_string1) != str:
#             continue
#         else:
#             education =  r"(?:1\.|2\.)\s*(.+?)\d{4}/\d{2}/\d{2}"
#             education_match = re.findall(education, input_string1, re.DOTALL)
#             if education_match:
#                 for e,eu in enumerate(education_match):
#                     df.loc[x,f'教育背景{numToCharater(str(e+1))}'] = eu
#     return df

