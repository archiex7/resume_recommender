from pathlib import Path
import pandas as pd
import glob
import os
import logging
import argparse
import warnings
import os
import yaml
from src.utility.utils import Logger, copy

warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:  # FIXME: Rain needs to check this in local (win) environment
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
# logger.log(f'config: {cfg}')

def find_excel_file(base_path, file_extension):
    return glob.glob(f'{base_path}{os.sep}*.{file_extension}')

def get_filename(str):
    filename = Path(str).stem
    return filename

def concat_str(df):
    # input_data = df[['職務名稱一', '職務名稱二', '職務名稱三', '職務名稱四', '職務名稱五', '職務名稱六', '職務名稱七', '職務名稱八','職務名稱九', '職務名稱十','職務類別一', '職務類別二', '職務類別三', '職務類別四',
    #     '職務類別五', '職務類別六', '職務類別七', '職務類別八', '職務類別九', '職務類別十', '工作內容一', '工作內容二', '工作內容三', '工作內容四', '工作內容五', '工作內容六', '工作內容七', '工作內容八',
    #     '工作內容九', '工作內容十','才能專長']]
    input_data = df[cfg['REC_CV']['INPUT_COLUMNS']['JOB_TITLES'] + cfg['REC_CV']['INPUT_COLUMNS']['JOB_CATS'] + cfg['REC_CV']['INPUT_COLUMNS']['JOB_CONTS'] + cfg['REC_CV']['INPUT_COLUMNS']['TALENT']]
    
    input_data_list = []
    for row in input_data.iterrows():
        tmp = ""
        for columns_name in input_data.columns:
            if pd.isna(row[1][columns_name]):
                pass
            else:
                tmp += row[1][columns_name]

        input_data_list.append(tmp)

    input_data = input_data.assign(resume_string=input_data_list)
    df = df.assign(resume_string=input_data_list)
    return df


def filter_freshman(df):
    df_over_120 = df[df['resume_string'].str.len() >= 120]
    df_under_120 = df[df['resume_string'].str.len() < 120]
    return df_over_120, df_under_120


def pdf_to_other(df, init_path, output_path):
    freshman_name = list(df[cfg['ALL_CV']['FILE_NAMES']])
    path_other = f"{output_path}{os.sep}其他"
    if not os.path.exists(path_other):
        os.makedirs(path_other)
    for name in freshman_name:
        copy(from_path=f'{init_path}{os.sep}{name}.pdf', to_path=f'{path_other}{os.sep}{name}.pdf')


def get_similarity_positions(criteria_knowledge_base, row, num):
    """
    Retrieves similar positions and their scores for a given row in a DataFrame.

    Args:
        criteria_knowledge_base: The knowledge base containing position information.
        row: The target row (e.g., resume_string).
        num: Number of similar positions to retrieve.

    Returns:
        A list of similar position names and their corresponding similarity scores.
    """
    target = str(row)
    similar_positions = criteria_knowledge_base.similarity_search_with_score(target, num)
    position_names = [pos[0].metadata['source'] for pos in similar_positions]
    similarity_scores = [pos[1] for pos in similar_positions]
    return position_names, similarity_scores

