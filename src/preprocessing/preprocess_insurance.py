import pandas as pd
import numpy as np 
import re
import os
import glob

'''regex in presprocess'''
def regex_sub(df):
    for t in range(len(df)):
        df[t] = re.sub('https?://[^ ]+|[\d/]+ [上下]午\d+:\d+', '',str(df[t]))
        df[t] = re.sub('https?://[^ ]+|[\d/]+ 晚上\d+:\d+', '',str(df[t]))
        df[t] = re.sub(r'專案成就(.*?)(?=。)','',str(df[t]))
        df[t] = str(df[t]).replace('\n', ' ').replace('*','').replace('附件','')
    return df
