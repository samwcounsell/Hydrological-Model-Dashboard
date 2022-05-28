from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

from components.navbar import create_navbar

navbar = create_navbar()

df = pd.read_csv('data/Feb_2020.csv')

min_val = 0
max_val = 1000

x_options = ['Arable_CMax', 'Arable_Evap', 'Arable_VarDist', 'Grassland_CMax', 'Grassland_Evap', 'Grassland_VarDist',
             'Forestry_CMax', 'Forestry_Evap', 'Forestry_VarDist', 'Urban_CMax', 'Urban_Evap', 'Urban_FTCoeff',
             'Class_5_STCoeff', 'Class_5_SoilTension', 'Class_7_STCoeff', 'Class_7_GWCoeff', 'Class_7_SoilTension',
             'Class_1_FTCoeff', 'Class_5_FTCoeff', 'Class_7_FTCoeff']

y_options = ['NSE_full_range', 'LogNSE_full_range', 'MARE', 'LogMARE', 'RMSE', 'VolError(%)']

# Page layout
layout = html.Div([

    navbar,
    dcc.Dropdown(id='x_dropdown', options=x_options, value = 'Arable_CMax', style = {'width': 400, 'textAlign': 'center'}),
    dcc.Dropdown(id='y_dropdown', options=y_options, value='VolError(%)', style = {'width': 400, 'textAlign': 'center'}),
    dcc.Dropdown(id='z_dropdown', options=y_options, value='RMSE', style = {'width': 400, 'textAlign': 'center'}),
    dcc.Graph(id='fig_B', style = {'width': '100%', 'height': 1000}),
    dcc.RangeSlider(id='slider_B',min=min_val, max=max_val, value = [min_val, max_val])

])


# Callback for figure A
@callback(
    [Output('slider_B', 'min'),
     Output('slider_B', 'max')],
    Input('x_dropdown', 'value'))


def update_RS(x_value):
    min_val = df[x_value].min()
    max_val = df[x_value].max()
    print(min_val, max_val)
    return min_val, max_val

@callback(
     Output('fig_B', 'figure'),
    [Input('x_dropdown', 'value'),
     Input('y_dropdown', 'value'),
     Input('z_dropdown', 'value'),
     #Input('slider_B', 'min'),
     #Input('slider_B', 'max'),
     Input('slider_B', 'value')])
# Function to create and update map depending on stage selected
def update_B(x_value, y_value, z_value, range):

    low, high = range
    mask = (df[df[x_value].between(low, high)])

    fig_B = px.scatter(mask, x=x_value, y=y_value, color=z_value, color_continuous_scale='ylgnbu')

    return fig_B
