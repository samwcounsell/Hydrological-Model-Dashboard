from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from components.navbar import create_navbar

navbar = create_navbar()

layout = html.Div([

    navbar,

    html.P(" "),
    html.P("App to visualise data produced by Kestrel-IHM"),
    html.P("Current quantiles for QQ-Plot (Observed) are as follows: Q1: 10.177, Q5: 4.72, Q10: 2.65, Q30: 0.995, "
           "Q50: 0.614, Q70: 0.412, Q90: 0.258, Q95: 0.217, Q99: 0.175"),
    html.P("The interactive plots can be found on the 'Plots' page and 'About' contains further information about the "
           "app and its capabilities."),
    html.P("On occasion when initialising the app, the top left and bottom left plots don't load, this can be "
           "resolved by simply updating the file path input box, i.e. deleting and retyping the a in data.")

])