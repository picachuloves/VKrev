import dash_core_components as dcc
import dash_html_components as html
from dash_extensions import Download
import dash_bootstrap_components as dbc

layout = html.Div([
    html.Br(),
    html.Div([
        html.H1(id='name'),
        html.Div(
            [html.Button("Скачать фрейм", id="btn_txt", className='btn btn-primary'), Download(id="download")]),
        html.Div([
            html.A([html.Button("На главную", className='btn btn-primary')], href='http://localhost:5000/index')
        ])
        ],
        className='container',
        style={'justify-content': 'space-between', 'display': 'flex'}
    ),
    html.Br(),
    html.Div([
        dbc.Card([
            html.H5('Количество отзывов', className='card-header'),
            dbc.CardBody([
                # html.H5('Количество отзывов', className='card-header'),
                html.Div([
                    html.P(id='rev_count', className="card-text", style={'width': '25%'}),
                    html.I(className="bi bi-chat-left-text")
                    ],
                    className='container',
                    style={'justify-content': 'space-between', 'display': 'flex'}
                )
            ]
            )
        ],
            className='text-dark bg-info mb-3',
            style={'height': '100%', 'width': '25%'}
        ),
        dbc.Card([
            html.H5('Количество человек', className='card-header'),
            dbc.CardBody([
                html.Div([
                    html.P(id='count_people', className="card-text"),
                    html.I(className="bi bi-people")
                ],
                    className='container',
                    style={'justify-content': 'space-between', 'display': 'flex'}
                )
                ])
        ],
            className='text-dark bg-info mb-3',
            style={'height': '100%', 'width': '25%'}
        ),
        dbc.Card([
            html.H5('Средняя оценка', className='card-header'),
            dbc.CardBody([
                html.Div([
                    html.P(id='rate', className="card-text"),
                    html.I(className="bi bi-star")
                ],
                    className='container',
                    style={'justify-content': 'space-between', 'display': 'flex'}
                )
                ])
        ],
            className='text-dark bg-info mb-3',
            style={'height': '100%', 'width': '25%'}
        )
    ],
        className='container',
        style={'justify-content': 'space-between', 'display': 'flex'}
    ),
    html.Br(),
    html.Div([
        dbc.Card([
            html.Div([
                dbc.Card([
                    html.Span([
                        dcc.Checklist(
                            id='deactivated',
                            options=[
                                {'label': 'Активные пользователи', 'value': 'active'},
                                {'label': 'Удаленные пользователи', 'value': 'deleted'},
                                {'label': 'Забаненные пользователи', 'value': 'banned'}
                            ],
                            value=['active', 'deleted', 'banned'],
                            className='form-check',
                            labelStyle={'margin-right': '10px', 'display': 'block'})
                        ],
                        className='border-left border-info')
                ]),
                html.Br(),
                dbc.Card([
                    html.Span([
                        dcc.Checklist(
                            id='sentiment',
                            options=[
                                {'label': 'Положительные отзывы', 'value': 1},
                                {'label': 'Отрицательные отзывы', 'value': 0}
                            ],
                            value=[1, 0],
                            className='form-check',
                            labelStyle={'margin-right': '10px', 'display': 'block'}
                        )],
                            className='border-left border-info')
                ],
                    style={'height': '60%'}),
                dcc.DatePickerRange(
                    id='date_range'
                    # min_date_allowed=df['date'].min().date(),
                    # max_date_allowed=static_callbacks.get_end_date(),
                    # start_date=static_callbacks.get_start_date(),
                    # end_date=static_callbacks.get_end_date()
                )
            ],
                className='container',
                style={'justify-content': 'space-between, left', 'display': 'flex'}
            ),
            html.Br(),
            html.Div([
                dcc.Graph(id='graph', figure={}, style={'height': '100%', 'width': '40%'}),
                dcc.Graph(id='sex-graph', figure={}, style={'height': '100%', 'width': '40%'})
            ],
                className='container',
                style={'justify-content': 'space-between', 'display': 'flex'}
            ),
            html.Div([
                dcc.Graph(id='cities', figure={}, style={'height': '100%', 'width': '60%'}),
                dcc.Graph(id='countries', figure={}, style={'height': '100%', 'width': '60%'})
                ],
                className='container',
                style={'justify-content': 'space-between', 'display': 'flex'}
            ),
            html.Div([
                dcc.Graph(id='age_graph', figure={}, style={'height': '100%', 'width': '70%'}),
                dcc.Graph(id='sp_graph', figure={}, style={'height': '100%', 'width': '70%'})
                ],
                className='container',
                style={'justify-content': 'space-between', 'display': 'flex'}
            ),
            html.Div([
                dbc.Toast(
                    [html.P(children=[], className="mb-0", id='most_neg')],
                    header="Самое негативное мнение",
                    style={'height': '80%', 'width': '100%', "maxWidth": "2000px"}
                ),
                dbc.Toast(
                    [html.P(children=[], className="mb-0", id='most_pos')],
                    header="Самое положительное мнение",
                    style={'height': '80%', 'width': '100%', "maxWidth": "2000px"}
                )
                ]
                    # className='row',
                    # style={'justify-content': 'space-between', 'display': 'flex'}
                )
            ],
            className='border border-info',
            style={'width': '90%', 'height': '100%'}
        )
        ],
        style={'justify-content': 'center', 'display': 'flex'}
    )
],
    className='container-fluid'
)
