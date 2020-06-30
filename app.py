import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from flask_talisman import Talisman

import datahandler.JHU
import datahandler.WorldBank
import datetime as dt

country_level_data = datahandler.JHU.global_case_data()
countries_list = country_level_data.columns
countries_of_interest = {'Asia': ['Bahrain', 'Singapore'],
                         'Europe': ['United Kingdom', 'Germany', 'Italy', 'Sweden'],
                         'North America': ['Canada', 'US', 'Mexico'],
                         'Oceania': ['New Zealand', 'Australia'],
                         'South America': ['Argentina', 'Brazil', 'Ecuador']
                         }
latest_wb_pop = datahandler.WorldBank.latest_worldbank("SP.POP.TOTL")
cases_per_capita = datahandler.WorldBank.calculate_case_rate(country_level_data,
                                                             latest_wb_pop
                                                             )

def confirmed_cases(country, df=country_level_data):
    return go.Scatter(x=df.index, y=df[country], name=country)

def regional_cases_graph(region, country):
    return dcc.Graph(figure={'data': [confirmed_cases(x) for x in country],
                             'layout': {'title': 'Time series of confirmed cases in ' + region,
                                        'showlegend': True
                                        }
                             },
                     id=('COVID-19 in ' + region)
                     )

def regional_cases_graph_per_capita(region, country):
    return dcc.Graph(figure={'data': [confirmed_cases(x, cases_per_capita) for x in country],
                             'layout': {'title': 'Time series of confirmed cases per million people in ' + region,
                                        'showlegend': True
                                        }
                             },
                     id=('COVID-19 per capita in ' + region)
                     )

# Content Security Policy Fix from https://github.com/plotly/dash/issues/630#issuecomment-605523528
import hashlib
import base64
from typing import List

def calculate_inline_hashes(app: dash.Dash) -> List[str]:
    """Given a Dash app instance, this function calculates
    CSP hashes (sha256 + base64) of all inline scripts, such that
    one of the biggest benefits of CSP (banning general inline scripts)
    can be utilized.

    Warning: Note that this function uses a "private" Dash app attribute,
    app._inline_scripts, which might change from one Dash version to the next.
    """
    return [
        f"'sha256-{base64.b64encode(hashlib.sha256(script.encode('utf-8')).digest()).decode('utf-8')}'"
        for script in [app.renderer] + app._inline_scripts
    ]

# app starts here

app = dash.Dash(__name__)

csp = {
    "default-src": ["'self'"],
    "script-src": ["'self'"] + calculate_inline_hashes(app),
    #"style-src": ["'self'", "'unsafe-inline'"]
}

server = Talisman(app.server, content_security_policy=csp)
#server = app.server

app.layout = html.Div(children=[
                                   html.H1(children='Personalised Dashboard for COVID-19 monitoring',
                                           style={'textAlign': 'center'}
                                           ),
                                   html.Div(children='''This page maintains a dashboard for my personal observations of the spread of the virus.'''),
                                   html.H2(children='Global cases:'),
                                   html.Div(children=[html.Span(f"As of {country_level_data.index[-1]}, there are "),
                                                      html.B(f"{country_level_data.sum(axis=1)[-1]:,} confirmed cases globally. "),
                                                      html.Span(f"This data was updated "),
                                                      html.B(f"{(dt.date.today() - country_level_data.index[-1]).days} day(s) ago.")
                                                      ]
                                            ),
                                   dcc.Graph(figure={'data': [go.Scatter(x=country_level_data.index,
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
                                               html.Tbody(html.Tr([html.Td(f"{country_level_data.iloc[-1][x]:,}"
                                                                           f"(+{country_level_data.diff().iloc[-1][x]:,.0f})"
                                                                           f"(+{country_level_data.pct_change().iloc[-1][x]:,.3f}%)"
                                                                           ) for sl in countries_of_interest.values() for x in sl]))
                                               ]),
                               ] + [html.Div(regional_cases_graph(k, v),
                                             style={'width': '49%',
                                                    'display': 'inline-block'}
                                             ) for (k, v) in countries_of_interest.items()
                                    ] + [html.H3(children='Cases per capita')] + [html.Div(regional_cases_graph_per_capita(k, v),
                                                                                           style={'width': '49%',
                                                                                                  'display': 'inline-block'}
                                                                                           ) for (k, v) in countries_of_interest.items()
                                                                                  ]
                      )

if __name__ == '__main__':
    app.run_server(debug=True)
