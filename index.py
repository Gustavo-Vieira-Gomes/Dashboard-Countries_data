from app import *
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('countries-of-the-world-clean.csv')
df_dicionario = df.to_dict()


#Opções Dropdown
options = [x for x in df['Region'].unique()]
options.append('GLOBAL')

# temas
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.SKETCHY

template1 = 'vapor'
template2 = 'sketchy'


app.layout = dbc.Container([
    dcc.Store('dataset_base', data=df_dicionario),
    # Linha 1
    dbc.Row([
        # Card de controle
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H3('Region Analysis')
                ]),
                dbc.CardBody([
                    dash_bootstrap_templates.ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
                    dcc.Dropdown(
                        options=options,
                        value='GLOBAL',
                        id='dropdown-regioes',
                        className='dbc',
                        style={'margin-top':'20px'}
                    ),
                ], style={'padding-top':'80px'})
            ], style={'height': '100%'})
        ], md=2),
        # Renda per Capta
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend('Renda Per Capita'),
                    html.H6('Maiores GDP'),
                    dcc.Graph(id='gdp-rich-graph', config={'showTips':False, 'displayModeBar':False}),
                    html.H6('Menores GDP'),
                    dcc.Graph(id='gdp-poor-graph', config={'showTips':False, 'displayModeBar':False})
                ])
            ])
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Taxas de Alfabetização')
                        ]),
                    dbc.Row([
                        dbc.Col([
                        html.H6('Mais alfabetizados'),
                        dcc.Graph(id='alfabetizacao-rich-graph', config={'showTips':True,'displayModeBar':False}),
                        html.H6('Menos alfabetizados'),
                        dcc.Graph(id='alfabetizacao-poor-graph', config={'showTips':True, 'displayModeBar': False})
                        ]),
                    ])
                    ])
                ])
            ])
        ], md=6)
    ],className='g-2 my-auto') ,

    # Linha 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([html.Legend('Taxa de Crescimento Populacional')]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='cresc-pop-graph', config={'showTips':False, 'displayModeBar':False}, style={'margin-top':'30px'})
                        ]),
                    ])
                ])
            ], style={'height':'100%'})
        ],md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.Legend('Fluxo Migratório')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Maiores taxas de Migração'),
                            dcc.Graph('migracao-rich-graph', config={'showTips':False, 'displayModeBar':False}),
                            html.H6('Menores taxas de Migração:'),
                            dcc.Graph('migracao-poor-graph', config={'showTips':False, 'displayModeBar':False})
                        ]),
                    ])
                ])
            ], style={'height':'100%'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.Legend('População da Região')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div(id='total-population'),
                            dcc.Graph('population-distribution-graph', style={'margin-top':'30px'})
                        ]),
                    ])
                ])
            ], style={'height': '100%'})
        ], md=3)
    ], className='g-2 my-auto')
], fluid=True)


############### Callbacks ###################
@app.callback(
    Output('gdp-rich-graph', 'figure'),
    Output('gdp-poor-graph', "figure"),
    Input('dropdown-regioes', 'value'),
    Input(dash_bootstrap_templates.ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('dataset_base', 'data')
)
def grafico_gdp(regiao, toggle, dataframe):
    template = template1 if toggle else template2
    df = pd.DataFrame(dataframe)
    if regiao != 'GLOBAL':
        df = df[df['Region'] == regiao]
    poor_countries = df.sort_values(by='GDP ($ per capita)').head(5)
    rich_countries = df.sort_values(by='GDP ($ per capita)').tail(5)

    fig = go.Figure()
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=poor_countries['GDP ($ per capita)'], y=poor_countries['Country'], name='menores gdp', orientation='h'))
    fig.add_trace(go.Bar(x=rich_countries['GDP ($ per capita)'], y=rich_countries['Country'], name='maiores gdp', orientation='h'))
    fig.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=120)
    fig2.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=120)

    return fig, fig2

@app.callback(
    Output('alfabetizacao-rich-graph', 'figure'),
    Output('alfabetizacao-poor-graph', 'figure'),
    Input('dropdown-regioes', 'value'),
    Input(dash_bootstrap_templates.ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('dataset_base', 'data')
)
def grafico_alfabetizacao(regiao, toggle, dataframe):
    template = template1 if toggle else template2
    df = pd.DataFrame(dataframe)
    if regiao != 'GLOBAL':
        df = df[df['Region'] == regiao]
    poor_countries = df.sort_values(by='Literacy (%)').head(5)
    rich_countries = df.sort_values(by='Literacy (%)').tail(5)
    fig_rich = go.Figure()
    fig_poor = go.Figure()
    fig_rich.add_trace(go.Bar(x=rich_countries['Country'], y=rich_countries['Literacy (%)'], name='maiores gdp'))
    fig_poor.add_trace(go.Bar(x=poor_countries['Country'], y=poor_countries['Literacy (%)'], name='maiores gdp'))
    fig_rich.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=120)
    fig_poor.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=120)
    
    return fig_rich, fig_poor

@app.callback(
    Output('cresc-pop-graph', 'figure'),
    Input('dropdown-regioes', 'value'),
    Input(dash_bootstrap_templates.ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('dataset_base', 'data')
)
def grafico_cresc(regiao, toggle, dataframe):
    template = template1 if toggle else template2
    df = pd.DataFrame(dataframe)
    if regiao != 'GLOBAL':
        df = df[df['Region'] == regiao]
    df['pop growth'] = df['Birthrate'] - df['Deathrate']
    poor_countries = df.sort_values(by='pop growth').head(5)
    rich_countries = df.sort_values(by='pop growth').tail(5)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=poor_countries['Country'], x=poor_countries['pop growth'], name='menores taxas', orientation='h'))
    fig.add_trace(go.Scatter(y=rich_countries['Country'], x=rich_countries['pop growth'], name='maiores taxas', orientation='h'))
    fig.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=200)

    return fig


@app.callback(
    Output('migracao-rich-graph', 'figure'),
    Output('migracao-poor-graph', 'figure'),
    Input('dropdown-regioes', 'value'),
    Input(dash_bootstrap_templates.ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('dataset_base', 'data')
)
def grafico_migracao(regiao, toggle, dataframe):
    template = template1 if toggle else template2
    df = pd.DataFrame(dataframe)
    if regiao != 'GLOBAL':
        df = df[df['Region'] == regiao]
    poor_countries = df.sort_values(by='Net migration').head(5)
    rich_countries = df.sort_values(by='Net migration').tail(5)
    fig_poor = go.Figure()
    fig_poor.add_trace(go.Bar(x=poor_countries['Country'], y=poor_countries['Net migration']))
    fig_rich = go.Figure()
    fig_rich.add_trace(go.Bar(x=rich_countries['Country'], y=rich_countries['Net migration']))
    fig_poor.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=120)
    fig_rich.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=120)

    return fig_rich, fig_poor

@app.callback(
    Output('total-population', 'children'),
    Output('population-distribution-graph', 'figure'),
    Input('dropdown-regioes', 'value'),
    Input(dash_bootstrap_templates.ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('dataset_base', 'data')
)
def population_function(regiao, toggle, dataframe):
    template = template1 if toggle else template2
    df = pd.DataFrame(dataframe)
    if regiao != 'GLOBAL':
        df = df[df['Region'] == regiao]
    total_population = df['Population'].sum()
    maiores_population = df.sort_values(by='Population').tail(5)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=maiores_population['Country'], y=maiores_population['Population']))
    fig.update_layout({'margin':{'l':0, 'r':0, 't':10, 'b':0}},template=template, height=200)
    retorno_population = f'TOTAL: {total_population:6,d}'
    return retorno_population, fig


if __name__ == '__main__':
    app.run(debug=True)
