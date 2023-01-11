import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/
# external_stylesheets = [dbc.themes.LUX]
# external_stylesheets = [dbc.themes.YETI]
# external_stylesheets = [dbc.themes.CYBORG]
external_stylesheets = [dbc.themes.FLATLY]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

server = app.server

memory_uid = None

