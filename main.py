import dash
import dash_auth
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly
from dash.dependencies import Input, Output, State
from base_nadzor.pages import main_page, rsn_layout, settings_layout, vvod_layout, new_rnv_layout, rnv_editor
from base_nadzor.app import app

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Главная", href="/home"),
        dbc.DropdownMenuItem("Разрешения на строительство", href="/rns"),
        dbc.DropdownMenuItem("Разрешения на ввод", href="/rnv"),
        dbc.DropdownMenuItem("Настройки", href="/settings"),
    ],
    nav=True,
    in_navbar=True,
    label="Меню"
)

navbar = dbc.NavbarSimple(
    children=[
        dropdown,
        dbc.NavItem(dbc.NavLink("Главная", href="#")),
        dbc.NavItem(dbc.NavLink("О программе", href="#"))
    ],
    brand="УПРАВЛЕНИЕ АРХИТЕКТУРЫ И ГРАДОСТРОИТЕЛЬСТВА г.Махачкалы",
    brand_href="#",
    color="primary",
    dark=True,
    links_left=False
)

# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#             html.A(
#                 # Use row and col to control vertical alignment of logo / brand
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Img(src=app.get_asset_url("gerb_png.png"), height="70px")),
#                         dbc.Col(dbc.NavbarBrand("Надзор", className="ml-2")),
#                     ],
#                     align="center"
#                 ),
#                 href="/home",
#             ),
#             dbc.NavbarToggler(id="navbar-toggler"),
#             dbc.Collapse(
#                 dbc.Nav(
#                     # right align dropdown menu with ml-auto className
#                     [dropdown], className="ml-auto", navbar=True
#                 ),
#                 id="navbar-collapse",
#                 navbar=True,
#             ),
#         ]
#     ),
#     color="dark",
#     # color="rgb(0,114,206)",
#     dark=True,
#     # className="navbar navbar-expand-lg navbar-dark bg-dark"
# )


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'admin'
}

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return main_page.layout
    elif pathname == '/rns':
        return rsn_layout.layout
    elif pathname == '/settings':
        return settings_layout.layout
    elif pathname == '/rnv':
        return vvod_layout.layout
    elif pathname == '/new_rnv':
        return new_rnv_layout.layout
    elif pathname == '/rnv_editor':
        return rnv_editor.layout


if __name__ == '__main__':
    app.run_server(debug=True)
