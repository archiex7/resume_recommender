import pandas as pd
import logging
import argparse
import warnings
import os
import yaml
from src.utility.utils import Logger
from src.preprocessing.cvtemplate_version import seniorityTemplate

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile: 
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
# logger.log(f'config: {cfg}')


def process_seniority(con_df):
    st_template = seniorityTemplate()
    
    seniority = []
    senior = con_df[cfg['REC_CV']['INPUT_COLUMNS']['WORK_EXPERIENCE']['NAME']]
    for se in senior:
        temp_seniority = st_template.seniority_parser(input_str=se)[cfg['REC_CV']['INPUT_COLUMNS']['SENIORITY']['NAME']]
        length = st_template.seniority_parser(input_str=se)[cfg['REC_CV']['INPUT_COLUMNS']['SENIORITY']['LENGTH']]
    
        temp_seniorities = temp_seniority + [None] * (10 - length)
        temp_seniorities = temp_seniorities[0:10]  # to ensure there are only 10 elements
        # final answer
        seniority.append(temp_seniorities)
    con_df[cfg['REC_CV']['INPUT_COLUMNS']['SENIORITY']['NAME']] = seniority
    con_df[[col for col in cfg['REC_CV']['INPUT_COLUMNS']['WORK_SENIORITY']]] = pd.DataFrame(con_df[cfg['REC_CV']['INPUT_COLUMNS']['SENIORITY']['NAME']].tolist(), index= con_df.index)

    return con_df
