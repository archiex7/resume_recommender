import os
import datetime
import pandas as pd

def selected_folder_date(init_path, today, todayDate):
    
    two_weeks_ago = today - datetime.timedelta(weeks=2)
    # 轉換日期格式以符合資料夾命名規則
    two_weeks_ago_str = two_weeks_ago.strftime('%Y%m%d')
    # 獲取當前工作目錄下的所有資料夾
    folders = [d for d in os.listdir(init_path) if os.path.isdir(os.path.join(init_path, d))]
    # 篩選出在指定日期範圍內的資料夾
    selected_folders = [f for f in folders if two_weeks_ago_str <= f <= todayDate]
    
    return selected_folders 


def filter_duplicates(selected_folder, class_file_name, df):
    for select_f in selected_folder:
        folder_path = f'.{os.sep}data{os.sep}output{os.sep}{select_f}'
        csv_file = pd.read_csv(f'{folder_path}{os.sep}{class_file_name}.csv')
        names_in_df = df['name'].isin(csv_file['name'])
        # 移除在 df['name'] 中的名字
        df = df[~names_in_df]
    return df
    

# a = selected_folder("C:/Users/J0713/Desktop/resume_recommender_project/data/output")
# print(a)