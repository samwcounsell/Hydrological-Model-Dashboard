from dash import dcc, html, Input, Output, callback

from components.navbar import create_navbar

navbar = create_navbar()

layout = html.Div([

    navbar,

])