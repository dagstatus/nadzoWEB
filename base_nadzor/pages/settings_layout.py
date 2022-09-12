import dash
import dash_auth
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly
from base_nadzor.app import app
import base_nadzor.settings_nadzor.settings as settings
from dash.dependencies import Input, Output, State

SettingsClass = settings.SettingsNadzor()


def make_setting_div():
    result_arr = [
        html.H4('Настройки', id='settings_status'),
        dbc.Button("Сохранить", id='save_settings_button', color="success", className="me-1"),
        html.Br()]
    for key, value in SettingsClass.settings_labes_dict.items():
        result_arr.append(html.P(value, style={'margin': '3px'})),
        result_arr.append(dbc.Input(id=key, type="text", placeholder="", value=SettingsClass.settings_dict.get(key),
                                    style={'marginBottom': '10px'}))

    return result_arr


layout = html.Div([
            dbc.Container([
                dbc.Row(make_setting_div(), id='setting_div')
                            ])
                  ])

@app.callback(
    Output("settings_status", "children"), Output('setting_div', 'children'), [Input("save_settings_button", "n_clicks")],
    [State(key, 'value') for key, value in SettingsClass.settings_labes_dict.items()]
)
def on_button_click(n, *args):
    idx = 0
    if n is None:
        return "Настройки", make_setting_div()
    else:

        for key, value in SettingsClass.settings_dict.items():
            SettingsClass.settings_dict[key] = args[idx]
            idx += 1
        SettingsClass.save_settings()

        SettingsClass.__init__()
        return f"Настройки успешно сохранены", make_setting_div()