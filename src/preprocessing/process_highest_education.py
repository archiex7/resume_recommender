import pandas as pd
import logging
import argparse
import warnings
import os
import yaml
from src.utility.utils import Logger
from src.preprocessing.cvtemplate_version import highestEducationTemplate

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:  # FIXME: Rain needs to check this in local (win) environment
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
# logger.log(f'config: {cfg}')

def process_highest_education(con_df):
    highest_education_template = highestEducationTemplate()
    
    highest_education_list = []
    edu_one = con_df[cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['NAME']]
    for part in edu_one:
        temp_highest_edu = highest_education_template.highest_education_parser(input_str=part)[cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['EDU_DETAILS']]
        length = highest_education_template.highest_education_parser(input_str=part)[cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['LENGTH']]
    
        temp_highest_educations = temp_highest_edu + [None] * (3 - length)
        temp_highest_educations = temp_highest_educations[0:3]  # to ensure there are only 3 elements

        # final answer
        highest_education_list.append(temp_highest_educations)
    
    con_df[cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['HIGH_EDU']] = highest_education_list
    con_df[[col for col in cfg['REC_CV']['INPUT_COLUMNS']['EDU_HIGH_BG']]] = pd.DataFrame(con_df[cfg['REC_CV']['INPUT_COLUMNS']['HIGHEST_EDUCATION']['HIGH_EDU']].tolist(), index= con_df.index)

    return con_df
