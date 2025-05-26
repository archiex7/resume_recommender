import logging
import json
import requests
import time
import sys
import re
import pandas as pd
import argparse
import warnings
import os
import yaml
from src.utility.utils import Logger

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile: 
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
# logger.log(f'config: {cfg}')

class CvTemplate1:
    """
    職務名稱 工作內容 工作技能
    """

    def __init__(self):
        pass

    @staticmethod
    def job_title_parser(input_str):
        regex_ = r"職務名稱:(.*?)(?=工作內容)"  # TODO: be careful with font
        job_titles = re.findall(regex_, input_str, re.DOTALL)
        for j in range(len(job_titles)):
            job_titles[j] = job_titles[j].strip()
            if job_titles[j].isalpha():
                pass
            else:
                job_titles[j] = job_titles[j].split(' ')[0]
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']}": job_titles,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(job_titles)
        }
        # print(f'job_titles: {job_titles}')
        # print(f'len(job_titles): {len(job_titles)}')
        return ans
    
    @staticmethod
    def job_category_parser(input_str):
        regex_ = r"職務類別:(.*?)(?=管理責任)"
        job_category = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']}": job_category,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(job_category)
        }
        return ans
    
    @staticmethod
    def work_content_parser(input_str):
        regex_ = r"職務名稱:(.*?)(?=工作技能)"  # TODO: be careful with font
        work_contents = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']}": work_contents,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(work_contents)
        }
        return ans
    


class CvTemplate2:
    """
    職務名稱 薪資待遇 工作內容 工作技能
    """

    def __init__(self):
        pass

    @staticmethod
    def job_title_parser(input_str):
        regex_ = r"職務名稱:(.*?)(?=薪資待遇)"  # TODO: be careful with font
        job_titles = re.findall(regex_, input_str, re.DOTALL)
        for j in range(len(job_titles)):
            job_titles[j] = job_titles[j].strip()
            if job_titles[j].isalpha():
                pass
            else:
                job_titles[j] = job_titles[j].split(' ')[0]
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']}": job_titles,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(job_titles)
        }
        return ans
    
    @staticmethod
    def job_category_parser(input_str):
        regex_ = r"職務類別:(.*?)(?=管理責任)"
        job_category = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']}": job_category,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(job_category)
        }
        return ans
    
    @staticmethod
    def work_content_parser(input_str):
        regex_ = r"薪資待遇:(.*?)(?=工作技能)"  # TODO: be careful with font
        work_contents = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']}": work_contents,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(work_contents)
        }
        return ans


class CvTemplate3:
    """
    職務名稱 管理責任 薪資待遇 離職原因 工作內容 工作技能
    """

    def __init__(self):
        pass

    @staticmethod
    def job_title_parser(input_str):
        regex_ = r"職務名稱:(.*?)(?=管理責任)"  # TODO: be careful with font
        job_titles = re.findall(regex_, input_str, re.DOTALL)
        for j in range(len(job_titles)):
            job_titles[j] = job_titles[j].strip()
            if job_titles[j].isalpha():
                pass
            else:
                job_titles[j] = job_titles[j].split(' ')[0]
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_TITLE']}": job_titles,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(job_titles)
        }
        return ans

    @staticmethod
    def job_category_parser(input_str):
        regex_ = r"職務類別:(.*?)(?=公司規模)"
        job_category = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['JOB_CATEGORY']}": job_category,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(job_category)
        }
        return ans
    
    @staticmethod
    def work_content_parser(input_str):
        regex_ = r"離職原因:(.*?)(?=工作技能)"  # TODO: be careful with font
        work_contents = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['WORK_CONTENTS']}": work_contents,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['LENGTH']}": len(work_contents)
        }
        return ans


class ebTemplate:
    """
    教育背景
    """

    def __init__(self):
        pass

    @staticmethod
    def educational_background_parser(input_str):
        regex_ = r"(?:1\.|2\.)\s*(.+?)\d{4}/\d{2}/\d{2}"  # TODO: be careful with font
        eb = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['EDU_BACKGROUND']}": eb,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['LENGTH']}": len(eb)
        }
        return ans

class seniorityTemplate:
    """
    年資
    """

    def __init__(self):
        pass

    @staticmethod
    def seniority_parser(input_str):
        regex_ = r"\((\d+ ?年 ?\d+ ?個 ?⽉)\)"  # TODO: be careful with font
        sen = re.findall(regex_, input_str, re.DOTALL)
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['SENIORITY']['NAME']}": sen,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['SENIORITY']['LENGTH']}": len(sen)
        }
        return ans
    
class highestEducationTemplate:
    """
        教育背景一(最高學歷)
        1.學校
        2.科系
        3.學位
    """

    def __init__(self):
        pass

    @staticmethod
    def highest_education_parser(input_str):
        parts = input_str.split()
        ans = {
            f"{cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['EDU_DETAILS']}": parts,
            f"{cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['LENGTH']}": len(parts)
        }
        return ans
    
# if __name__ == '__main__':
#     ver_1_str = '''1.
# 臺灣中⼩企業銀⾏股份有限公司 , 2021/02/01 ~ 2021/06/01 (0年5個⽉)
# 產業類別: 公司規模:
# 職務類別: ⼯讀⽣ 管理責任: 無
# 職務名稱: 實習⽣
# https://ehrweb.104.com.tw/inspect/resumeVip.do?print=1&pks=30000002766162&custNo=3374805000&similarIdNo=0&RM3.CSRF_TOKEN=06…1/32023/8/8 上午11:29 吳婕寧
# ⼯作內容:
# ⼯作技能:
# 迅杰科技股份有限公司 , 2019/07/01 ~ 2019/08/01 (0年2個⽉)
# 產業類別: 公司規模:
# 職務類別: ⼯讀⽣ 管理責任: 無
# 2.
# 職務名稱: ⼯讀⽣
# ⼯作內容:
# ⼯作技能:
#     '''
#     ver_2_str = '''1.
# 新安東京海上產物保險股份有限公司 , 2022/07/01 ~ 2023/05/01 (0年11個⽉)
# 產業類別: 產物保險業 公司規模: 500以上
# 職務類別: 理賠⼈員 管理責任: 無
# 職務名稱: ⾞險理賠 薪資待遇: 不公開
# ⼯作內容:
# file:///C:/Users/J0713/Desktop/保單⾏政/20231024/吳紀賢.htm 1/62023/10/25 上午9:54 吳紀賢.htm
# ⼯作技能:
# 台灣保全事業股份有限公司 , 2021/05/01 ~ 2022/06/01 (1年2個⽉)
# 產業類別: 陸上運輸輔助業 公司規模: 500以上
# 職務類別: 保全技術⼈員 管理責任: 4⼈以下
# 2. 職務名稱: 現⾦運送員 薪資待遇: 不公開
# 1.負責店家營業額現⾦運送總公司清點
# ⼯作內容: 2.銀⾏⾦流紙鈔銅板運送台銀營業部庫存和各分⾏調撥現⾦運送
# 3.銀⾏提款機補鈔，故障排除等服務。
# ⼯作技能: 運輸路線規劃管理,簽收╱驗收作業,庫存管理規劃作業,點收╱代收貨款作業
# 富邦⼈壽保險股份有限公司(總公司) , 2020/01/01 ~ 2021/01/01 (1年1個⽉)
# 產業類別: ⼈⾝保險業 公司規模: 30~100
# 職務類別: 核保／保險內勤⼈員 管理責任: 無
# 職務名稱: ⾏銷專員&核保⼈員 薪資待遇: 不公開
# 3. 1.⾏銷專員: 幫助客⼾做好醫療理財和各式各樣的⽣活規劃，讓客⼾知道保險的重要性，不要
# 因為意外比明天先到⽽損失錢財。也幫忙客⼾做好投資資產管理，協助外幣投資理財等⼯具，
# 並協助客⼾做好汽機⾞保險維護⾃⼰的權益，以勉發⽣狀況時不知所措⽽財損。
# ⼯作內容:
# 2.核保⼈員: 審核客⼾要申請理賠時所需要文件有無跟實際相符公司可承擔風險資格，確定保
# 險費率的流程，並按標的物危險分級，制定及核定費率規劃，給予不同費率保證業務質量，增
# 加保險經營穩定性。
# ⼯作技能:
# 茶之漾茶坊 , 2017/04/01 ~ 2019/06/01 (2年3個⽉)
# 產業類別: 飲料店業 公司規模: 1~30
# 職務類別: 活動企劃 管理責任: 無
# 各活動承辦負責⼈、市場訂單&茶葉
# 職務名稱: 薪資待遇: 不公開
# 開發訂單業務負責⼈
# 1.活動承辦負責: 負責各節慶活動規劃擺設項⽬、決定季節性飲品分析顧客喜愛味覺是否符合
# 4.
# 經濟效益，並帶領其他同事分⼯合作宣傳執⾏；去各個⼯業區舉辦活動熱⾨商品試喝、發傳單
# 規畫優惠已增基⼤客⼾訂購量。
# 2.茶葉介紹擺設&市場訂單業務開發負責: 茶葉依回⽢、熟青、海拔等作歸類，並製作牌⼦已
# ⼯作內容: 讓客⼾選茶葉⼀⽬瞭然，並製作簡報將茶包裝跟茶葉禮盒做詳細介紹並讓客⼾在最短時間內挑
# 選到⾃⼰想的茶葉；安排時間出外拜訪客⼾並介紹⾃家茶葉促成交。
# 3.傳統市場訂單業務負責⼈: 登記訂單並做歸納依時間將訂單送達客⼾⼿中，每天excel紀錄
# 訂單明細跟業績狀況並開會做檢討改善，規畫活動增加訂單讓顧客養成依賴製造忠實客⼾以廣
# ⼤介紹客源。
# ⼯作技能:
# '''
#     ver_4_str = '''https://ehrweb.104.com.tw/inspect/resume1.do?print=1&RM3.CSRF_TOKEN=ec63704c-9797-486d-98ee-5fa2c0583f6c 1/62023/1/16 下午3:27 劉⼦立
# Albert-Ludwigs-Universität Freiburg 德國弗萊堡⼤學 , 2021/09/01 ~ 2021/ 累積⼯作經歷:
# 11/01 (0年3個⽉) 助教: 1年以下
# 產業類別:⼤專校院教育事業 公司性質:本國企業 研究助理: 1~2
# 年
# 職務類別:助教 公司規模:500以上
# 統計學研究員: 1
# Teaching assistant 統計學助
# 職務名稱: 管理責任:無 年以下
# 1.
# 教
# 其他資訊專業⼈
# 薪資待遇:不公開 離職原因: 員: 1年以下
# 研究所課程"Statistics with R"之課程助教，內容包含：
# ⼯作內容:- 統計學理論
# - 利⽤R語⾔程式撰寫進⾏統計分析應⽤與實作
# ⼯作技能:⾏政事務處理,R,⽣物統計學,資料分析
# Swiss TPH 瑞⼠公共衛⽣與熱帶醫學研究院 , 2021/04/01 ~ 2021/12/01 (0年9
# 個⽉)
# 產業類別:其他專業／科學及技術業 公司性質:本國企業
# 職務類別:研究助理 公司規模:500以上
# 職務名稱:Research assistant 研究助理管理責任:無
# 薪資待遇:不公開 離職原因:
# 2. - 執⾏碩⼠論文研究計畫：「統計模型與機器學習⽅法應⽤於瑞⼠⼆氧化氮濃度
# 時間與空間分佈模型之比較——併⽤⼟地利⽤回歸模型LUR與衛星遙測資料(A
# comparison of statistical and machine-learning approaches for spatio
# ⼯作內容:temporal modeling of nitrogen dioxide across Switzerland: with land
# use regression and satellite-derived data)」（成績：1.5 excellent）
# - 應⽤資料科學於環境衛⽣研究的實例
# - Data ETL, Spatial data processing, modeling, validation, prediction
# R,Python,撰寫研究報告與論文,申請與執⾏研究計畫,Machine Learning,軟體
# ⼯作技能:
# 程式設計
# Helmholtz Zentrum für Umweltforschung 亥姆霍茲環境研究中⼼ , 2020/11/0
# 1 ~ 2021/02/01 (0年4個⽉)
# 產業類別:其他專業／科學及技術業 公司性質:本國企業
# 職務類別:統計學研究員 公司規模:500以上
# 職務名稱:Research Data Analyst 管理責任:無
# 薪資待遇:不公開 離職原因:
# - 資料分析：統計量化分析、時間序列分析
# 3.
# - 研究軟體開發
# ｜資料處理ETL (extraction, transformation, loading)流程⾃動化
# ｜開發資料前處理與資料QC程式
# ⼯作內容:｜開發互動式資料視覺化使⽤者介⾯ (RShiny)
# - 我開發的資料平台：(1) 使團隊中每個成員（來⾃不同領域與專業背景、本⾝
# 不熟悉程式）都可以以簡單的UI輕鬆取⽤處理好的實驗資料；(2) 顯著降低PM
# 的⼯作負荷；(3)降低團隊成員間的溝通成本，因此(4) 有效加速整個專案的進
# 程。
# ⼯作技能:GIS,R,Python,ArcGis,HTML,統計軟體操作
# https://ehrweb.104.com.tw/inspect/resume1.do?print=1&RM3.CSRF_TOKEN=ec63704c-9797-486d-98ee-5fa2c0583f6c 2/62023/1/16 下午3:27 劉⼦立
# Helmholtz Zentrum für Umweltforschung 亥姆霍茲環境研究中⼼ , 2020/08/0
# 1 ~ 2020/10/01 (0年3個⽉)
# 產業類別:其他專業／科學及技術業 公司性質:本國企業
# 職務類別:其他資訊專業⼈員 公司規模:500以上
# 職務名稱:Research Intern 管理責任:無
# 薪資待遇:不公開 離職原因:
# 4.
# - 資料分析：統計量化分析、時間序列分析
# - 研究軟體開發
# ｜資料處理ETL (extraction, transformation, loading)流程⾃動化
# ⼯作內容:｜開發資料前處理與資料QC程式
# ｜開發互動式資料視覺化使⽤者介⾯ (RShiny)
# - 協助實地實驗與資料搜集（主動式通風與室內氡氣污染之⼯程改善）
# - 使⽤R與QGIS進⾏空間資料處理
# ⼯作技能:
# 財團法⼈⼯業技術研究院 , 2018/07/01 ~ 2018/08/01 (0年2個⽉)
# 產業類別:檢測技術服務 公司性質:本國企業
# 職務類別:研究助理 公司規模:500以上
# 職務名稱:實習⽣ 管理責任:無
# 5. 薪資待遇:不公開 離職原因:
# - 分析空氣品質資料並執⾏研究專題「松⼭機場硫氧化物排放對台北市空氣品質
# 影響之探討」。專題成果海報於2018年台灣公共衛⽣年會發表。
# ⼯作內容:
# - 開發資料處理與資料分析程式
# - 地理資訊系統與空間資料處理
# ⼯作技能:GIS,申請與執⾏研究計畫,撰寫研究報告與論文,Python,文書處理軟體操作
# 國立臺灣⼤學 空間巨量資料計畫 , 2017/04/01 ~ 2017/06/01 (0年3個⽉)
# 產業類別:⼤專校院教育事業 公司性質:本國企業
# 職務類別:研究助理 公司規模:500以上
# 職務名稱:學習型助理 管理責任:無
# 6.
# 薪資待遇:不公開 離職原因:
# 使⽤R與Google Earth Pro進⾏空間資料處理，包括資料品質過濾與前處理、
# ⼯作內容:
# geocoding
# ⼯作技能:GIS
# '''
#     ver_3_str = ''
#     cv_template_1 = CvTemplate1()
#     cv_template_2 = CvTemplate2()
#     cv_template_3 = CvTemplate3()
#     job_titles = list()
#     work_contents = list()
#     df = pd.DataFrame({'work_experience': [ver_1_str, ver_2_str, ver_3_str, ver_4_str]})
#     work_exps = df['work_experience']
#     for work_exp in work_exps:
#         temp_job_titles = cv_template_1.job_title_parser(input_str=work_exp)['job_titles']
#         temp_work_contents = cv_template_1.work_content_parser(input_str=work_exp)['work_contents']
#         length = cv_template_1.job_title_parser(input_str=work_exp)['length']
#         if length == 0:
#             pass
#         else:
#         # check which template
#             first_item = temp_job_titles[0]
#             if ('管理責任' not in first_item) and ('薪資待遇' not in first_item) and ('離職原因' not in first_item):  # template 1
#                 pass
#             elif ('管理責任' not in first_item) and ('薪資待遇' in first_item) and ('離職原因' not in first_item):  # template 2
#                 temp_job_titles = cv_template_2.job_title_parser(input_str=work_exp)['job_titles']
#                 temp_work_contents = cv_template_2.work_content_parser(input_str=work_exp)['work_contents']
#                 length = cv_template_2.job_title_parser(input_str=work_exp)['length']
#             elif ('管理責任' in first_item) and ('薪資待遇' in first_item) and ('離職原因' in first_item):  # template 3
#                 temp_job_titles = cv_template_3.job_title_parser(input_str=work_exp)['job_titles']
#                 temp_work_contents = cv_template_3.work_content_parser(input_str=work_exp)['work_contents']
#                 length = cv_template_3.job_title_parser(input_str=work_exp)['length']
#         # fill the list until the certain length
#         temp_job_titles = temp_job_titles + [None] * (10 - length)
#         temp_work_contents = temp_work_contents + [None] * (10 - length)
#         # final answer
#         job_titles.append(temp_job_titles)
#         work_contents.append(temp_work_contents)
#     df['job_titles'] = job_titles
#     df[['job_title_1', 'job_title_2', 'job_title_3', 'job_title_4', 'job_title_5',
#         'job_title_6', 'job_title_7', 'job_title_8', 'job_title_9', 'job_title_10']] = pd.DataFrame(df['job_titles'].tolist(), index=df.index)

#     df['work_contents'] = work_contents
#     df[['work_content_1', 'work_content_2', 'work_content_3', 'work_content_4', 'work_content_5',
#         'work_content_6', 'work_content_7', 'work_content_8', 'work_content_9', 'work_content_10']] = pd.DataFrame(df['work_contents'].tolist(), index=df.index)
#     df.to_csv('output.csv', index=False, encoding='utf-8-sig')
