import dash
import dash_auth
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly
from base_nadzor.app import app

layout = html.Div([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),
    dcc.Dropdown(['A', 'B'], 'A', id='dropdown'),
    dcc.Graph(id='graph')
], className='container')


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph(dropdown_value):
    return {
        'layout': {
            'title': 'Graph of {}'.format(dropdown_value),
            'margin': {
                'l': 20,
                'b': 20,
                'r': 10,
                't': 60
            }
        },
        'data': [{'x': [1, 2, 3], 'y': [4, 1, 2]}]

    }
