from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from components.navbar import create_navbar

navbar = create_navbar()

layout = html.Div([

    navbar,

    html.P(" "),
    html.P(" App to visualise data produced by Hydrological Models"),
    html.P(" The interactive plots can be found on the 'Plots' page and 'About' contains further information about the "
           "app and its capabilities."),
    html.P(" On occasion when initialising the app, the top left and bottom left plots don't load, this can be "
           "resolved by simply updating the file path input box, i.e. deleting and retyping the a in data.")

])