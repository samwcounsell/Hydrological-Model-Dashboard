from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

from components.navbar import create_navbar

navbar = create_navbar()

df = pd.read_csv('data/Feb_2020.csv')

x_options = ['Arable_CMax', 'Arable_Evap', 'Arable_VarDist''Grassland_CMax', 'Grassland_Evap', 'Grassland_VarDist',
             'Forestry_CMax', 'Forestry_Evap', 'Forestry_VarDist', 'Urban_CMax', 'Urban_Evap', 'Urban_FTCoeff',
             'Class_5_STCoeff', 'Class_5_SoilTension', 'Class_7_STCoeff', 'Class_7_GWCoeff', 'Class_7_SoilTension',
             'Class_1_FTCoeff', 'Class_5_FTCoeff', 'Class_7_FTCoeff']

y_options = ['NSE_full_range', 'LogNSE_full_range', 'MARE', 'LogMARE', 'RMSE', 'VolError(%)']

# Page layout
layout = html.Div([

    navbar,
    dcc.Dropdown(id='x_dropdown', options=x_options, value='Arable_CMax'),
    dcc.Dropdown(id='y_dropdown', options=y_options, value='VolError(%)'),
    dcc.Graph(id='fig_A', style = {'width': '100%', 'height': 1000}),

])


# Callback for figure A
@callback(
    Output('fig_A', 'figure'),
    [Input('x_dropdown', 'value'),
     Input('y_dropdown', 'value')])

# Function to create and update map depending on stage selected
def update_A(x_value, y_value):
    fig_A = px.scatter(df, x=x_value, y=y_value)

    return fig_A
