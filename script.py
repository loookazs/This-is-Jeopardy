import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
jeopardy = pd.read_csv('jeopardy.csv')

# changing column names
jeopardy.columns = ['Show Number', 'Air Date', 'Round', 'Category', 'Value',
                    'Question', 'Answer']

# changing data type in column 'Value' to float
jeopardy['Value'] = pd.to_numeric(jeopardy.apply(lambda row: "".join([i for i in row['Value'] if i.isdigit()]), axis=1))

# search for words in jeopardy df
def word_search(word_list):
    matching_questions_df = pd.DataFrame()
    for i in word_list:
        i = i.lower()
        matching_questions_df[i] = jeopardy.apply(lambda row: row['Question'] if i in row['Question'].lower().split() else np.nan, axis=1)
    matching_questions_df = matching_questions_df.dropna()
    for i in list(matching_questions_df.keys()):
        if list(matching_questions_df.keys()).index(i) != 0:
            matching_questions_df.pop(i)
    matching_questions_df.columns = ['Question']
    return pd.merge(matching_questions_df, jeopardy, how ='inner')


def average(df_name, column_name):
    return df_name[column_name].mean()

def unique_answers(word_list):
    analyzed_df = word_search(word_list)
    return analyzed_df.groupby('Answer').count().sort_values(by = ['Question'], ascending = False)

def filter_by_date(data_frame, data_frame_date_column, start_date, end_date):
    data_frame[data_frame_date_column] = data_frame.apply(lambda row: row[data_frame_date_column] if start_date < row[data_frame_date_column] < end_date else None, axis = 1)
    data_frame = data_frame.dropna()
    return data_frame

# grouping by 'Category' and 'Round'
category_stats_per_round = jeopardy.groupby(['Category', 'Round'])['Show Number'].count().reset_index()
