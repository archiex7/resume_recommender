import logging
import sys
import os
import pdfplumber
import pandas as pd
real_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{real_path}")
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from src.preprocessing.cvtemplate_version import *



def process_educational_background(con_df):
    eb_template_1 = ebTemplate()
    
    edu_background = []
    edu_bg = con_df['教育背景']
    for edu in edu_bg:
        temp_edu_bg = eb_template_1.educational_background_parser(input_str=edu)['edu_background']
        length = eb_template_1.educational_background_parser(input_str=edu)['length']
    
        temp_edu_bgs = temp_edu_bg + [None] * (5 - length)
        # final answer
        edu_background.append(temp_edu_bgs)
    con_df['edu_background'] = edu_background
    con_df[['教育背景一', '教育背景二', '教育背景三', '教育背景四', '教育背景五']] = pd.DataFrame(con_df['edu_background'].tolist(), index= con_df.index)

    
    return con_df