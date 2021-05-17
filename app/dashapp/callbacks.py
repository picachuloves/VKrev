import pandas as pd
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px
from datetime import datetime
from flask_login import current_user
from dash_extensions.snippets import send_data_frame
from app.dashapp import static_callbacks
from app.classifier import Classifier


df = pd.DataFrame()

def register_callbacks(dashapp):
    # df = pd.read_excel('results/otz.xlsx')

    @dashapp.callback([Output(component_id='sex-graph', component_property='figure'),
                       Output(component_id='cities', component_property='figure'),
                       Output(component_id='countries', component_property='figure'),
                       # Output(component_id='most_user', component_property='children'),
                       Output(component_id='graph', component_property='figure'),
                       Output(component_id='age_graph', component_property='figure'),
                       Output(component_id='sp_graph', component_property='figure'),
                       Output(component_id='name', component_property='children'),
                       Output(component_id='rev_count', component_property='children'),
                       Output(component_id='count_people', component_property='children'),
                       Output(component_id='rate', component_property='children'),
                       Output(component_id='date_range', component_property='start_date'),
                       Output(component_id='date_range', component_property='end_date'),
                       Output(component_id='most_neg', component_property='children'),
                       Output(component_id='most_pos', component_property='children')],
                      [Input(component_id='sentiment', component_property='value'),
                       Input(component_id='deactivated', component_property='value'),
                       Input(component_id='date_range', component_property='start_date'),
                       Input(component_id='date_range', component_property='end_date')])
    def update_graph(sentiment, deactivated, start_date, end_date):
        print(pd.to_datetime('today'))
        static_callbacks.init()
        pathname = f"results/{current_user.id}/{current_user.name}"
        global df
        df = pd.read_excel(f'{pathname}/otz.xlsx')
        print(pd.to_datetime('today'))
        dff = df.copy()
        dff = dff[dff['sentiment'].isin(sentiment)].reset_index(drop=True)
        dff = dff[dff['deactivated'].isin(deactivated)].reset_index(drop=True)
        dff['date'] = pd.to_datetime(dff['date'])
        # if is not None
        if start_date and end_date:
            dff = dff[(dff['date'].dt.date >= pd.to_datetime(start_date).date())
                      & (dff['date'].dt.date <= pd.to_datetime(end_date).date())]

        dff_sex = dff.groupby(['sex']).agg({'id_comment': 'count'}) \
            .rename({'id_comment': 'Количество'}, axis=1).reset_index()
        fig_sex = px.pie(dff_sex, names='sex', values='Количество', title='Распределение по полу')
        fig_sex.update_traces(textinfo='value+percent')

        dff_cities = dff[dff['city'] != 'Не указано'].groupby(['city']).agg({'id_comment': 'count'}) \
            .rename({'id_comment': 'Количество'}, axis=1).reset_index()
        fig_cities = px.histogram(x=dff_cities['city'], y=dff_cities['Количество'],
                                  title=f"Город (указан у {dff[dff['city'] != 'Не указано']['city'].count()} человек)",
                                  labels={'x': 'Города', 'y': 'Количество'})

        dff_countries = dff[dff['country'] != 'Не указано'].groupby(['country']).agg({'id_comment': 'count'}) \
            .rename({'id_comment': 'Количество'}, axis=1).reset_index()
        fig_countries = px.histogram(dff_countries, x='country', y='Количество',
                                     title=f"Страна (указана у {dff[dff['country'] != 'Не указано']['country'].count()} человек)",
                                     labels={'country': 'Страны', 'y': 'Количество'})

        # most_user = dff.groupby(['user_id']).agg({'id_comment': 'count'}) \
        #     .rename({'id_comment': 'Количество'}, axis=1).sort_values('Количество', ascending=False)\
        #     .reset_index().head(1)
        # most_user_id = most_user['user_id'][0]
        # most_user_count = most_user['Количество'][0]
        # dff_most_user = dff[dff['user_id'] == most_user_id]
        # most_user_div = f'Больше всего комментариев от {dff_most_user["name"].iloc[0]}: {most_user_count}. ' \
        #                 f'{dff_most_user["sentiment"].mean() * 100} % отзывов положительны.'

        dff_fig = dff.groupby(['sentiment']).agg({'id_comment': 'count'}) \
            .rename({'id_comment': 'Количество'}, axis=1).reset_index()
        dff_fig.loc[dff_fig['sentiment'] == 0, 'sentiment'] = 'Негативные'
        dff_fig.loc[dff_fig['sentiment'] == 1, 'sentiment'] = 'Положительные'
        fig = px.pie(dff_fig, names='sentiment', values='Количество', title='Отзывы')
        fig.update_traces(textinfo='value+percent')

        dff_age = dff.copy()
        dff_age.loc[(datetime.now().year - dff_age['bdate_year']) <= 18, 'age_g'] = '< 18'
        dff_age.loc[((datetime.now().year - dff_age['bdate_year']) > 18) &
                    ((datetime.now().year - dff_age['bdate_year']) <= 30), 'age_g'] = '19-30'
        dff_age.loc[((datetime.now().year - dff_age['bdate_year']) > 30) &
                    ((datetime.now().year - dff_age['bdate_year']) <= 45), 'age_g'] = '31-45'
        dff_age.loc[((datetime.now().year - dff_age['bdate_year']) > 45), 'age_g'] = '> 46'
        dff_age = dff_age.groupby(['age_g']).agg({'id_comment': 'count'}) \
            .rename({'id_comment': 'Количество'}, axis=1).reset_index()
        fig_age = px.pie(dff_age, names='age_g', values='Количество',
                         title=f"Возраст (указан у {dff['bdate_year'].notnull().sum()} человек)",
                         labels={'age_g': 'Возраст'})

        dff_sp = dff[dff['relation'] != 'не указано'].groupby(['relation']).agg({'id_comment': 'count'}) \
            .rename({'id_comment': 'Количество'}, axis=1).reset_index()
        fig_sp = px.pie(dff_sp, names='relation', values='Количество',
                        title=f"Семейное положение (указано у {dff[dff['relation'] != 'не указано']['relation'].count()} человек)")

        # classifier = Classifier()
        # most_neg_i, most_pos_i = classifier.get_most(dff)
        # most_neg = dff.iloc[most_neg_i]['text']
        # most_pos = dff.iloc[most_pos_i]['text']
        print(pd.to_datetime('today'))
        return fig_sex, fig_cities, fig_countries, fig, fig_age, fig_sp, \
               current_user.name, df.shape[0], len(df['user_id'].unique()), round(df['sentiment'].mean(), 3), \
               df['date'].min().date(), df['date'].max().date(), \
               df[df['most'] == 0]['text'].values[0], df[df['most'] == 1]['text'].values[0]


    @dashapp.callback(
        Output("download", "data"),
        Input("btn_txt", "n_clicks"),
        prevent_initial_call=True,
    )
    def func(n_clicks):
        return send_data_frame(df.to_excel, "mydf.xlxs", sheet_name="Sheet_name_1")
