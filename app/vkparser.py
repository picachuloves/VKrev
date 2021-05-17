import vk
import math
import pandas as pd
from flask_login import current_user
from pathlib import Path
import requests
import time

class VkParser:
    api = None

    def __init__(self):
        if current_user.is_authenticated:
            session = vk.Session(access_token=current_user.token)
            self.api = vk.API(session=session)

    def new_api(self, token):
        if self.api is None:
            session = vk.Session(access_token=token)
            self.api = vk.API(session=session)

    def load(self, group_id, board_id, count, name):
        cel = count // 2000
        b = []
        drob = math.ceil((count - cel * 2000) / 100)
        for i in range(cel):
            b.append(20)
        b.append(drob)
        res = pd.DataFrame()
        print(pd.to_datetime('today'))
        for i in range(cel + 1):
            inner_count = b[i]
            req = f"""var i = 0;
                              var ans = [];
                              while (i != {inner_count}) {{
                              ans.splice( i * 100, 0, API.board.getComments({{"group_id": {group_id}, "topic_id": {board_id}, "need_likes": 1, "count": 100, "offset": (i + {i * 20}) * 100}}).items);
                              i = i + 1;
                              }};
                              return ans;
                    """
            #
            connect_loop = True
            while connect_loop:
                try:
                    test = self.api.execute(code=req, v=5.95)
                    connect_loop = False
                except requests.exceptions.ReadTimeout:
                    print("\n Переподключение к серверам ВК \n")
                    time.sleep(3)
                    continue
            for j in range(len(test)):
                res = pd.concat([res, pd.DataFrame(test[j])])
        print(pd.to_datetime('today'))
        res = res[(res['text'] != '') & (res['from_id'] > 0)].reset_index(drop=True)
        ids = res['from_id'].unique().tolist()
        ids = [str(int) for int in ids]
        users_count = len(ids)
        cel = math.ceil(users_count / 1000)
        profiles = pd.DataFrame()
        for i in range(cel):
            ids_ = ",".join(ids[i * 1000: (i + 1) * 1000])
            test = self.api.users.get(user_ids=ids_, fields='bdate, city,country,occupation,relation,sex',
                                    offset=i * 1000, v=5.95)
            profiles = pd.concat([profiles, pd.DataFrame(test)])
        profiles = profiles.reset_index(drop=True)
        result = pd.merge(res, profiles, how='left', left_on='from_id', right_on='id')
        result['date'] = pd.to_datetime(result['date'], unit='s')
        result.loc[result['relation'] == 1, 'relation'] = 'не женат/не замужем'
        result.loc[result['relation'] == 2, 'relation'] = 'есть друг/есть подруга'
        result.loc[result['relation'] == 3, 'relation'] = 'помолвлен/помолвлена'
        result.loc[result['relation'] == 4, 'relation'] = 'женат/замужем'
        result.loc[result['relation'] == 5, 'relation'] = 'всё сложно'
        result.loc[result['relation'] == 6, 'relation'] = 'в активном поиске'
        result.loc[result['relation'] == 7, 'relation'] = 'влюблён/влюблена'
        result.loc[result['relation'] == 8, 'relation'] = 'в гражданском браке'
        result.loc[result['relation'] == 0, 'relation'] = 'не указано'
        result['relation'] = result['relation'].fillna('не указано')
        cities = result.loc[result['city'].notnull(), ['id_x', 'city']]
        cities['city'] = [d['title'] for d in cities['city']]
        result = pd.merge(result, cities, how='left', on='id_x')
        result = result.rename({'city_y': 'city'}, axis=1)
        result = result.drop('city_x', 1)
        result['city'] = result['city'].fillna('Не указано')
        countries = result.loc[result['country'].notnull(), ['id_x', 'country']]
        countries['country'] = [d['title'] for d in countries['country']]
        result = pd.merge(result, countries, how='left', on='id_x')
        result = result.rename({'country_y': 'country'}, axis=1)
        result = result.drop('country_x', 1)
        result['country'] = result['country'].fillna('Не указано')
        result['likes'] = [d['count'] for d in result['likes']]
        result['deactivated'] = result['deactivated'].fillna('active')
        result.loc[result['sex'] == 0, 'sex'] = 'Не указано'
        result.loc[result['sex'] == 1, 'sex'] = 'Женский'
        result.loc[result['sex'] == 2, 'sex'] = 'Мужской'
        result.loc[result['bdate'].notnull(), 'bdate_day'] = [d[0] for d in
                                                              result.loc[result['bdate'].notnull(), 'bdate'].str.split(
                                                                  '.')]
        result.loc[result['bdate'].notnull(), 'bdate_month'] = [d[1] for d in result.loc[
            result['bdate'].notnull(), 'bdate'].str.split('.')]
        result.loc[result['bdate'].notnull(), 'bdate_year'] = [d[2] if 2 < len(d) else None for d in
                                                               result.loc[result['bdate'].notnull(), 'bdate'].str.split(
                                                                   '.')]
        result_ = result.rename({'id_x': 'id_comment', 'from_id': 'user_id'}, axis=1)
        result_['name'] = result_['first_name'] + ' ' + result_['last_name']
        result_ = result_[
            ['id_comment', 'user_id', 'date', 'text', 'name', 'deactivated', 'sex', 'is_closed', 'bdate_day',
             'bdate_month', 'bdate_year', 'city', 'country', 'relation']]
        path = rf"results/{current_user.id}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        result_.to_excel(f'{path}/otz.xlsx', index=False)
        return path


    def check_groups(self):
        groups = self.api.groups.get(user_id=current_user.id, filter='moder', v=5.21)
        count = groups['count']
        groups_ids = groups['items']
        return groups

