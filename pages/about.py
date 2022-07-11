from dash import dcc, html, Input, Output, callback

from components.navbar import create_navbar

navbar = create_navbar()

layout = html.Div([

    navbar,

    html.P(" "),
    html.P(" Data Types: Currently only works with csv files"),
    html.P(" Works for any number of input variables as long as the number and order of Quantile columns, and number "
           "of Output columns remain fixed."),
    html.P(" "),
    html.P(" Any of the input or output variables can be on both axis of the three scatter plots, range slider inputs "
           "apply to every graph (including QQ-Plot)."),
    html.P(" "),
    html.P(" To be added: Range slider for z-axis (gradient), click to isolate trace on the plot and corresponding "
           "scatter points.")

])