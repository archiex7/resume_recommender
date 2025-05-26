from src.preprocessing.cvtemplate_version import *


def process_seniority(con_df):
    st_template = seniorityTemplate()
    
    seniority = []
    senior = con_df['工作經驗']
    for se in senior:
        temp_seniority = st_template.seniority_parser(input_str=se)['seniority']
        length = st_template.seniority_parser(input_str=se)['length']
    
        temp_seniorities = temp_seniority + [None] * (10 - length)
        # final answer
        seniority.append(temp_seniorities)
    con_df['seniority'] = seniority
    con_df[['工作經驗年資一', '工作經驗年資二', '工作經驗年資三', '工作經驗年資四', '工作經驗年資五',
            '工作經驗年資六', '工作經驗年資七', '工作經驗年資八', '工作經驗年資九', '工作經驗年資十']] = pd.DataFrame(con_df['seniority'].tolist(), index= con_df.index)

    
    return con_df