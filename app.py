import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import datahandler.JHU

country_level_data = datahandler.JHU.global_case_data()
countries_list = country_level_data.columns
countries_of_interest = {'Asia': ['Bahrain', 'Singapore'],
                         'Europe': ['United Kingdom', 'Germany', 'Italy', 'Sweden'],
                         'Oceania': ['New Zealand', 'Australia'],
                         'South America': ['Argentina', 'Brazil', 'Ecuador']
                         }

def confirmed_cases(country):
    return go.Line(x=country_level_data.index, y=country_level_data[country], name=country)

def regional_cases_graph(region, country):
    return dcc.Graph(figure={'data': [confirmed_cases(x) for x in country],
                             'layout': {'title': 'Time series of confirmed cases in ' + region,
                                        'showlegend': True
                                        }
                             },
                     id=('COVID-19 in ' + region)
                     )

app = dash.Dash(__name__)

app.layout = html.Div(children=[
                                   html.H1(children='Personalised Dashboard for COVID-19 monitoring',
                                           style={'textAlign': 'center'}
                                           ),
                                   html.Div(children='''This page maintains a dashboard for my personal observations of the spread of the virus.'''),
                                   html.H2(children='Global cases:'),
                                   html.Div(children=[html.Span(f"As of {country_level_data.index[-1]}, there are "),
                                                      html.B(f"{country_level_data.sum(axis=1)[-1]:,} confirmed cases globally.")
                                                      ]
                                            ),
                                   dcc.Graph(figure={'data': [go.Line(x=country_level_data.index,
                                                                     y=country_level_data.sum(axis=1),
                                                                     name='Confirmed cases'
                                                                     )], # expects a dict
                                                     'layout': {'title': 'Global time series of confirmed cases',
                                                                'showlegend': True
                                                                }
                                                     },
                                             id='global'
                                             ),
                                   html.H2(children='Country-level specifics:'),
                                   html.H3(children='Headline figures:'),
                                   html.Table([html.Thead(html.Tr([html.Th(x) for sl in countries_of_interest.values() for x in sl])),
                                               html.Tbody(html.Tr([html.Td(f"{country_level_data.iloc[-1][x]:,}") for sl in countries_of_interest.values() for x in sl]))
                                               ]),
                               ] + [html.Div(regional_cases_graph(k, v),
                                             style={'width': '49%',
                                                    'display': 'inline-block'}
                                             ) for (k, v) in countries_of_interest.items()
                                    ]
                      )

if __name__ == '__main__':
    app.run_server(debug=True)
