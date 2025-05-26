import pandas as pd
import logging
import argparse
import warnings
import os
import yaml
from src.utility.utils import Logger
from src.preprocessing.cvtemplate_version import ebTemplate

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", help="env to execute, e.g. dev, pa, prod")
args = parser.parse_args()

logger = Logger(name="main program", log_file=None, log_level=logging.INFO)

with open(f".{os.sep}configs{os.sep}{args.env}_config.yml", "r", encoding='UTF-8') as ymlfile:  # FIXME: Rain needs to check this in local (win) environment
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
# logger.log(f'config: {cfg}')

def process_educational_background(con_df):
    eb_template_1 = ebTemplate()
    
    edu_background = []
    edu_bg = con_df[cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['NAME']]
    for edu in edu_bg:
        temp_edu_bg = eb_template_1.educational_background_parser(input_str=edu)[cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['EDU_BACKGROUND']]
        length = eb_template_1.educational_background_parser(input_str=edu)[cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['LENGTH']]
    
        temp_edu_bgs = temp_edu_bg + [None] * (5 - length)
        temp_edu_bgs = temp_edu_bgs[0:5]  # to ensure there are only 5 elements
        # final answer
        edu_background.append(temp_edu_bgs)
    con_df[cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['EDU_BACKGROUND']] = edu_background
    con_df[[col for col in cfg['REC_CV']['INPUT_COLUMNS']['EDU_BGS']]] = pd.DataFrame(con_df[cfg['REC_CV']['INPUT_COLUMNS']['EDUCATIONAL_BACKGROUND']['EDU_BACKGROUND']].tolist(), index= con_df.index)

    return con_df
