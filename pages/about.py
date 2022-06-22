from dash import dcc, html, Input, Output, callback

from components.navbar import create_navbar

navbar = create_navbar()

layout = html.Div([

    navbar,

    html.P("Data Types: Currently only works with csv files"),
    html.P("Works for any number of input variables as long as the number and order of Quantile columns, and number "
           "of Output columns remain fixed.")

])