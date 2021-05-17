import pandas as pd
from flask_login import current_user


df = pd.read_excel(f'results/otz.xlsx')

def init():
    path = f"results/{current_user.id}/{current_user.name}"
    global df
    df = pd.read_excel(f'{path}/otz.xlsx')

def most_neg():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    dff = df.copy()
    neg = dff[dff['most'] == 0]['text'].values[0]
    return neg


def most_pos():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    dff = df.copy()
    pos = dff[dff['most'] == 1]['text'].values[0]
    return pos


def get_name():
    # return current_user.name
    return 'kkk'


def get_size():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return df.shape[0]


def get_people():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return len(df['user_id'].unique())


def get_mean_rate():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return round(df['sentiment'].mean(), 3)


def get_has_age():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return f"Указан возраст у {df['bdate_year'].notnull().sum()} человек"


def get_has_not_age():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return f"Не указан возраст у {df['bdate_year'].isnull().sum()} человек"


def get_start_date():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return df['date'].min().date()


def get_end_date():
    # path = f"results/{current_user.id}/{current_user.name}"
    # df = pd.read_excel(f'{path}/otz.xlsx')
    return df['date'].max().date()
