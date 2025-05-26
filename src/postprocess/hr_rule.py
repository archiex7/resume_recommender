# -*- coding: utf-8 -*-

class Age:
    @staticmethod
    def annotate(pdf, position):
        if position == '理賠審核人員':
            # print(f'1: {position}')
            # print(f'{list(pdf["年齡"])}, {len(list(pdf["年齡"]))}')
            pass
        elif position == '核保人員':
            pass
        elif position == '保全服務部專案人員':
            threshold = 30
            pdf.loc[
                (pdf['年齡'] > threshold)
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: age > {threshold};"
        elif position == '保單行政人員':
            threshold = 30
            pdf.loc[
                (pdf['年齡'] > threshold)
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: age > {threshold};"
        elif position == '客服人員':
            threshold = 40
            pdf.loc[
                (pdf['年齡'] > threshold)
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: age > {threshold};"
        else:
            pass
        return pdf


class Education:
    """
    columns of the input dataframe
    ['年齡', '總年資', 'email', '手機', '工作經驗', '教育背景', '才能專長', '自我介紹', 'name',
   'seniority', '工作經驗年資一', '工作經驗年資二', '工作經驗年資三', '工作經驗年資四', '工作經驗年資五',
   '工作經驗年資六', '工作經驗年資七', '工作經驗年資八', '工作經驗年資九', '工作經驗年資十', 'job_titles',
   '職務名稱一', '職務名稱二', '職務名稱三', '職務名稱四', '職務名稱五', '職務名稱六', '職務名稱七', '職務名稱八',
   '職務名稱九', '職務名稱十', 'job_category', '職務類別一', '職務類別二', '職務類別三', '職務類別四',
   '職務類別五', '職務類別六', '職務類別七', '職務類別八', '職務類別九', '職務類別十', 'work_contents',
   '工作內容一', '工作內容二', '工作內容三', '工作內容四', '工作內容五', '工作內容六', '工作內容七', '工作內容八',
   '工作內容九', '工作內容十', 'edu_background', '教育背景一', '教育背景二', '教育背景三', '教育背景四',
   '教育背景五', 'resume_string', 'note', 'answer', 'score', 'ans1', 'ans2', 'score1', 'score2',
   'highest_education', '學校', '科系', '學位',
    ]

    ---
    partial sample data:
    'edu_background': ['輔仁⼤學 統計資訊學系 ⼤學 ', '國立臺北商業⼤學 應⽤外語科(組) 五專 ', None, None, None],
    '教育背景一': '輔仁⼤學 統計資訊學系 ⼤學 ',
    '教育背景二': '國立臺北商業⼤學 應⽤外語科(組) 五專 ',
    '教育背景三': None, '教育背景四': None, '教育背景五': None,
    '學校': '輔仁⼤學',
    '科系': '統計資訊學系',
    '學位': '⼤學'
    """
    @staticmethod
    def annotate(pdf, position):
        if position == '理賠審核人員':
            pdf.loc[
                (pdf['科系'].str.contains('餐飲|體育'))
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: 科系 為 餐飲|體育;"
        elif position == '核保人員':
            pdf.loc[
                (~pdf['學位'].str.contains('大學|university', case=False))  # FIXME: pdfplumber chinese character parsing issue: '⼤學' != '大學'
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: highest_education 為 大學以下;"
        elif position == '保全服務部專案人員':
            pdf.loc[
                (~pdf['學位'].str.contains('大學|university', case=False))
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: highest_education 為 大學以下;"
        elif position == '保單行政人員':
            pdf.loc[
                (~pdf['學位'].str.contains('大學|university', case=False))
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: highest_education 為 大學以下;"
        elif position == '客服人員':
            pdf.loc[
                (~pdf['學位'].str.contains('大學|university', case=False))
                & ((pdf['ans1'] == position) | (pdf['ans2'] == position)),
                'note'
            ] += f"不適任{position}: highest_education 為 大學以下;"
        else:
            pass
        return pdf
