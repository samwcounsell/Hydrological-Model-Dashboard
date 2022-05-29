from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.navbar import create_navbar
from functions.data_reading import pull_data

navbar = create_navbar()

df = pull_data()
vars = list(df)

q = vars[-9:]
y_options = vars[-17:-9]
del (y_options[2:4])
x_options = vars[:-17]

min_val = 0
max_val = 1000

# Page layout
layout = html.Div([

    navbar,
    html.H1(
        children=' Kestrel-IHM 3-Dimensional Plot',
        style={'textAlign': 'center', 'padding': 30}
    ),
    dbc.Row([
        dbc.Col(
            html.H6(children='x-axis Variable:'), width={'size': 2, 'offset': 4}
        ),
        dbc.Col(
            dcc.Dropdown(id='x_dropdown', options=x_options, value='Arable_CMax',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.H6(children='y-axis Variable:'), width={'size': 2, 'offset': 4}
        ),
        dbc.Col(
            dcc.Dropdown(id='y_dropdown', options=y_options, value='VolError(%)',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.H6(children='Gradient Variable:'), width={'size': 2, 'offset': 4}
        ),
        dbc.Col(
            dcc.Dropdown(id='z_dropdown', options=y_options, value='RMSE',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.H6(children='Log y-axis (QQ-Plot):'), width={'size': 2, 'offset': 4}
        ),
        dbc.Col(
            dcc.Dropdown(id='log_dropdown', options=['Yes', 'No'], value='No',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='fig', style={'width': '100%', 'height': 950}),
        ),
        dbc.Col(
            dcc.Graph(id='q_fig', style={'width': '100%', 'height': 950})
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.P(""),
        ),
        dbc.Col(
            html.P("x-axis Data Range:"),
        ),
        dbc.Col(
            dcc.RangeSlider(id='slider', min=min_val, max=max_val, value=[min_val, max_val])
        )
    ], style={"display": "grid", "grid-template-columns": "5% 10% 75%"})

])


# Callback for figure A
@callback(
    [Output('slider', 'min'),
     Output('slider', 'max')],
    Input('x_dropdown', 'value'))
def update_RS(x_value):
    min_val = df[x_value].min()
    max_val = df[x_value].max()
    return min_val, max_val


@callback(
    Output('fig', 'figure'),
    [Input('x_dropdown', 'value'),
     Input('y_dropdown', 'value'),
     Input('z_dropdown', 'value'),
     # Input('slider_B', 'min'),
     # Input('slider_B', 'max'),
     Input('slider', 'value')])
# Function to create and update map depending on stage selected
def update_B(x_value, y_value, z_value, range):
    low, high = range
    mask = (df[df[x_value].between(low, high)])

    fig = px.scatter(mask, x=x_value, y=y_value, color=z_value, color_continuous_scale='ylgnbu')

    return fig


@callback(
    Output('q_fig', 'figure'),
    [Input('x_dropdown', 'value'),
     Input('slider', 'value'),
     Input('log_dropdown', 'value')])
def update_main(x_value, range, log):
    low, high = range
    q_mask = (df[df[x_value].between(low, high)])

    q_fig = go.Figure()
    for idx, row in q_mask.iterrows():
        q_fig.add_trace(
            go.Scatter(
                x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                y=[row['Q1'], row['Q5'], row['Q10'], row['Q30'], row['Q50'], row['Q70'],
                   row['Q90'], row['Q95'], row['Q99']],
                mode="lines", showlegend=False
            )
        )
    q_fig.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                               y=[10.177, 4.72, 2.65, 0.995, 0.614, 0.412, 0.258, 0.217, 0.175], name="Observed",
                               marker_color='rgba(0,0,0,0.5)'))
    q_fig.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                               y=[10.177, 4.72, 2.65, 0.995, 0.614, 0.412, 0.258, 0.217, 0.175],
                               marker_color='rgba(0,0,0,0.5)', showlegend=False))
    q_fig.update_layout(xaxis=dict(title='Quantile'), yaxis=dict(title='Flow'))

    if log == 'Yes':
        q_fig.update_yaxes(title='Flow (Log)', type="log")

    else:
        q_fig.update_yaxes()

    return q_fig
