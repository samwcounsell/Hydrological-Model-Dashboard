from dash import dcc, html, Input, Output, callback, State, Dash
import dash_bootstrap_components as dbc
import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from components.navbar import create_navbar
from functions.data_reading import pull_data, get_quantiles

pd.set_option('display.max_columns', None)

navbar = create_navbar()

df = pull_data('data')
types = 'text'

vars = list(df)

# Seperating quantiles from variables
q = vars[-9:]
options = vars[:-9]

# Defining launch values for range sliders
min_val_tlx, min_val_tly, min_val_blx, min_val_bly, min_val_brx, min_val_bry = 0, -1, 0, -1, 0, -1
max_val_tlx, max_val_tly, max_val_blx, max_val_bly, max_val_brx, max_val_bry = 1000, 1000, 1000, 1000, 1000, 1000

# Custom Colour Scheme
trace_cols = ['seagreen', 'blue', 'cornflowerblue', 'lightgreen', 'forestgreen', 'gold', 'lightblue', 'lightgreen']

# Page layout
layout = html.Div([
    
    navbar,

    html.H1(
        children=' Hydrological Model 3-Dimensional Plot',
        style={'textAlign': 'center', 'padding': 30}
    ),

    # X, Y, Z       log
    dbc.Row([
        
        dbc.Col(dcc.Dropdown(id='tl_x_dropdown', options=options, value=options[0],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='tl_y_dropdown', options=options, value=options[-1],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='tl_z_dropdown', options=options, value=options[-2],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(html.P("")),
        dbc.Col(dcc.Dropdown(id='QQ_log_dropdown', options=['Log Axis: Yes', 'Log Axis: No'], value='Log Axis: No',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),

    ], style={"display": "grid", "grid-template-columns": "15% 15% 15% 20% 40%"}),
    
    # graph        graph
    dbc.Row([

        dbc.Col(
            dcc.Graph(id='tl_fig', style={'width': '100%', 'height': 700}),
        ),
        dbc.Col(
            dcc.Graph(id='QQ_plot', style={'width': '100%', 'height': 700}),
        )

    ]),

    # x slider
    dbc.Row([

        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='tlx_slider', min=min_val_tlx, max=max_val_tlx, value=[min_val_tlx, max_val_tlx])),
        dbc.Col(html.P("")),

        ], style={"display": "grid", "grid-template-columns": "5% 40% 55%"}),

    # y slider
    dbc.Row([

        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='tly_slider', min=min_val_tly, max=max_val_tly, value=[min_val_tly, max_val_tly])),
        dbc.Col(html.P("")),

        ], style={"display": "grid", "grid-template-columns": "5% 40% 55%"}),


    # X Y Z        X Y Z

    dbc.Row([

        dbc.Col(dcc.Dropdown(id='bl_x_dropdown', options=options, value=options[1],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='bl_y_dropdown', options=options, value=options[-1],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='bl_z_dropdown', options=options, value=options[-2],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(html.P("")),
        dbc.Col(dcc.Dropdown(id='br_x_dropdown', options=options, value=options[2],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='br_y_dropdown', options=options, value=options[-1],
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='br_z_dropdown', options=options, value=options[-2],
                         style={'textAlign': 'center', 'font-size': 'x-small'}))

    ], style={"display": "grid", "grid-template-columns": "15% 15% 15% 10% 15% 15% 15%"}),
    
    # graph        graph
    
    dbc.Row([

        dbc.Col(
            dcc.Graph(id='bl_fig', style={'width': '100%', 'height': 700}),
        ),
        dbc.Col(
            dcc.Graph(id='br_fig', style={'width': '100%', 'height': 700}),
        )

    ]),
    
    # slider      slider
    
    dbc.Row([

        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='blx_slider', min=min_val_blx, max=max_val_blx, value=[min_val_blx, max_val_blx])),
        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='brx_slider', min=min_val_brx, max=max_val_brx, value=[min_val_brx, max_val_brx]))

    ], style={"display": "grid", "grid-template-columns": "5% 40% 15% 40%"}),
    
    dbc.Row([

        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='bly_slider', min=min_val_bly, max=max_val_bly, value=[min_val_bly, max_val_bly])),
        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='bry_slider', min=min_val_bry, max=max_val_bry, value=[min_val_bry, max_val_bry]))

    ], style={"display": "grid", "grid-template-columns": "5% 40% 15% 40%"}),

    dbc.Row([

        dbc.Col(html.P(""))

    ]),

    dbc.Row([

        dbc.Col(html.P("Paste filepath below:", style={'textAlign': 'center'}))

    ]),

    # Data Collection
    dbc.Row([

        dbc.Col(html.P("")),
        dcc.Input(id="filepath", type='text', value='data', style={'fontsize': 'small'}),
        dbc.Col(html.P(""))

    ], style={"display": "grid", "grid-template-columns": "10% 80% 10%"}),

    dbc.Row([

        dcc.Store(id = 'memory')

    ])
    
])


# Data Callback
@callback(
    Output('memory', 'data'),
    Input('filepath', 'value')
)
def retrieve_data(filepath):
     df = pull_data(filepath)
     return df.to_json(orient='split')


# Dropdown Callbacks
@callback(
    Output('tl_x_dropdown', 'options'),
    Output('tl_y_dropdown', 'options'),
    Output('tl_z_dropdown', 'options'),
    Output('bl_x_dropdown', 'options'),
    Output('bl_y_dropdown', 'options'),
    Output('bl_z_dropdown', 'options'),
    Output('br_x_dropdown', 'options'),
    Output('br_y_dropdown', 'options'),
    Output('br_z_dropdown', 'options'),
    Output('tl_x_dropdown', 'value'),
    Output('tl_y_dropdown', 'value'),
    Output('tl_z_dropdown', 'value'),
    Output('bl_x_dropdown', 'value'),
    Output('bl_y_dropdown', 'value'),
    Output('bl_z_dropdown', 'value'),
    Output('br_x_dropdown', 'value'),
    Output('br_y_dropdown', 'value'),
    Output('br_z_dropdown', 'value'),
    Input('filepath', 'value')
)
def update_TLO(filepath):

    df = pull_data(filepath)
    vars = list(df)
    options = vars[:-9]
    non_constant = []
    for var in options:
        var_min, var_max = df[var].min(), df[var].max()
        range = var_max - var_min
        if range > 0:
            non_constant.append(var)



    return(non_constant, non_constant, non_constant, non_constant, non_constant, non_constant, non_constant, non_constant, non_constant,
           non_constant[0], non_constant[-1], non_constant[-2], non_constant[1], non_constant[-1], non_constant[-2], non_constant[2], non_constant[-1], non_constant[-2])


# Range Slider Updates
@callback(
    [Output('tlx_slider', 'min'),
     Output('tlx_slider', 'max'),
     Output('tlx_slider', 'value')],
    Input('tl_x_dropdown', 'value'),
    Input('filepath', 'value'))
def update_TLXS(x_value, filepath):
    df = pull_data(filepath)
    tlx_min_val = math.floor(df[x_value].min() * 1000) / 1000
    tlx_max_val = math.ceil(df[x_value].max() * 1000) / 1000
    return tlx_min_val, tlx_max_val, [tlx_min_val, tlx_max_val]


@callback(
    [Output('tly_slider', 'min'),
     Output('tly_slider', 'max'),
     Output('tly_slider', 'value')],
    Input('tl_y_dropdown', 'value'),
    Input('filepath', 'value'))
def update_TLYS(y_value, filepath):
    df = pull_data(filepath)
    tly_min_val = math.floor(df[y_value].min() * 1000) / 1000
    tly_max_val = math.ceil(df[y_value].max() * 1000) / 1000
    return tly_min_val, tly_max_val, [tly_min_val, tly_max_val]

@callback(
    [Output('blx_slider', 'min'),
     Output('blx_slider', 'max'),
     Output('blx_slider', 'value')],
    Input('bl_x_dropdown', 'value'),
    Input('filepath', 'value'))
def update_BLXS(x_value, filepath):
    df = pull_data(filepath)
    blx_min_val = math.floor(df[x_value].min() * 1000) / 1000
    blx_max_val = math.ceil(df[x_value].max() * 1000) / 1000
    return blx_min_val, blx_max_val, [blx_min_val, blx_max_val]

@callback(
    [Output('bly_slider', 'min'),
     Output('bly_slider', 'max'),
     Output('bly_slider', 'value')],
    Input('bl_y_dropdown', 'value'),
    Input('filepath', 'value'))
def update_BLYS(y_value, filepath):
    df = pull_data(filepath)
    bly_min_val = math.floor(df[y_value].min() * 1000) / 1000
    bly_max_val = math.ceil(df[y_value].max() * 1000) / 1000
    return bly_min_val, bly_max_val, [bly_min_val, bly_max_val]


@callback(
    [Output('brx_slider', 'min'),
     Output('brx_slider', 'max'),
     Output('brx_slider', 'value')],
    Input('br_x_dropdown', 'value'),
    Input('filepath', 'value'))
def update_BRXS(x_value, filepath):
    df = pull_data(filepath)
    brx_min_val = math.floor(df[x_value].min() * 1000) / 1000
    brx_max_val = math.ceil(df[x_value].max() * 1000) / 1000
    return brx_min_val, brx_max_val, [brx_min_val, brx_max_val]

@callback(
    [Output('bry_slider', 'min'),
     Output('bry_slider', 'max'),
     Output('bry_slider', 'value')],
    Input('br_y_dropdown', 'value'),
    Input('filepath', 'value'))
def update_BRYS(y_value, filepath):
    df = pull_data(filepath)
    bry_min_val = math.floor(df[y_value].min() * 1000) / 1000
    bry_max_val = math.ceil(df[y_value].max() * 1000) / 1000
    return bry_min_val, bry_max_val, [bry_min_val, bry_max_val]

# Standard plot Callbacks

# TL
@callback(
    Output('tl_fig', 'figure'),
    [Input('tl_x_dropdown', 'value'),
     Input('tl_y_dropdown', 'value'),
     Input('tl_z_dropdown', 'value'),
     Input('tlx_slider', 'value'),
     Input('tly_slider', 'value'),
     Input('bl_x_dropdown', 'value'),
     Input('bl_y_dropdown', 'value'),
     Input('bl_z_dropdown', 'value'),
     Input('blx_slider', 'value'),
     Input('bly_slider', 'value'),
     Input('br_x_dropdown', 'value'),
     Input('br_y_dropdown', 'value'),
     Input('br_z_dropdown', 'value'),
     Input('brx_slider', 'value'),
     Input('bry_slider', 'value'),
     Input('memory', 'data')
     ])

def update_tl_fig(mainx_value, mainy_value, mainz_value, mainx_range, mainy_range, bx_value, by_value, bz_value, bx_range, by_range, cx_value, cy_value, cz_value, cx_range, cy_range, data):

    df = pd.read_json(data, orient='split')


    mainx_low, mainx_high = mainx_range
    mainy_low, mainy_high = mainy_range
    bx_low, bx_high = bx_range
    by_low, by_high = by_range
    cx_low, cx_high = cx_range
    cy_low, cy_high = cy_range
    # Selecting only data within specified range slider values
    mask = (df[df[mainx_value].between(mainx_low, mainx_high) & df[mainy_value].between(mainy_low, mainy_high) &
               df[bx_value].between(bx_low, bx_high) &
               df[cx_value].between(cx_low, cx_high) & df[by_value].between(by_low, by_high) &
               df[cy_value].between(cy_low, cy_high)])

    tl_fig = px.scatter(mask, x=mainx_value, y=mainy_value, color=mainz_value, color_continuous_scale='viridis')

    return tl_fig

# BL
@callback(
    Output('bl_fig', 'figure'),
    [Input('bl_x_dropdown', 'value'),
     Input('bl_y_dropdown', 'value'),
     Input('bl_z_dropdown', 'value'),
     Input('blx_slider', 'value'),
     Input('bly_slider', 'value'),
     Input('tl_x_dropdown', 'value'),
     Input('tl_y_dropdown', 'value'),
     Input('tl_z_dropdown', 'value'),
     Input('tlx_slider', 'value'),
     Input('tly_slider', 'value'),
     Input('br_x_dropdown', 'value'),
     Input('br_y_dropdown', 'value'),
     Input('br_z_dropdown', 'value'),
     Input('brx_slider', 'value'),
     Input('bry_slider', 'value'),
     Input('memory', 'data')
     ])

def update_bl_fig(mainx_value, mainy_value, mainz_value, mainx_range, mainy_range, bx_value, by_value, bz_value,
                  bx_range, by_range, cx_value, cy_value, cz_value, cx_range, cy_range, data):

    df = pd.read_json(data, orient='split')
    
    mainx_low, mainx_high = mainx_range
    mainy_low, mainy_high = mainy_range
    bx_low, bx_high = bx_range
    by_low, by_high = by_range
    cx_low, cx_high = cx_range
    cy_low, cy_high = cy_range

    mask = (df[df[mainx_value].between(mainx_low, mainx_high) & df[mainy_value].between(mainy_low, mainy_high) & df[
        bx_value].between(bx_low, bx_high) &
               df[cx_value].between(cx_low, cx_high) & df[by_value].between(by_low, by_high) &
               df[cy_value].between(cy_low, cy_high)])

    bl_fig = px.scatter(mask, x=mainx_value, y=mainy_value, color=mainz_value, color_continuous_scale='viridis')

    return bl_fig

# BR
@callback(
    Output('br_fig', 'figure'),
    [Input('br_x_dropdown', 'value'),
     Input('br_y_dropdown', 'value'),
     Input('br_z_dropdown', 'value'),
     Input('brx_slider', 'value'),
     Input('bry_slider', 'value'),
     Input('tl_x_dropdown', 'value'),
     Input('tl_y_dropdown', 'value'),
     Input('tl_z_dropdown', 'value'),
     Input('tlx_slider', 'value'),
     Input('tly_slider', 'value'),
     Input('bl_x_dropdown', 'value'),
     Input('bl_y_dropdown', 'value'),
     Input('bl_z_dropdown', 'value'),
     Input('blx_slider', 'value'),
     Input('bly_slider', 'value'),
     Input('memory', 'data')
     ])

def update_br_fig(mainx_value, mainy_value, mainz_value, mainx_range, mainy_range, bx_value, by_value, bz_value,
                  bx_range, by_range, cx_value, cy_value, cz_value, cx_range, cy_range, data):

    df = pd.read_json(data, orient='split')

    mainx_low, mainx_high = mainx_range
    mainy_low, mainy_high = mainy_range
    bx_low, bx_high = bx_range
    by_low, by_high = by_range
    cx_low, cx_high = cx_range
    cy_low, cy_high = cy_range

    mask = (df[df[mainx_value].between(mainx_low, mainx_high) & df[mainy_value].between(mainy_low, mainy_high) &
               df[bx_value].between(bx_low, bx_high) & df[cx_value].between(cx_low, cx_high) &
               df[by_value].between(by_low, by_high) & df[cy_value].between(cy_low, cy_high)])

    br_fig = px.scatter(mask, x=mainx_value, y=mainy_value, color=mainz_value, color_continuous_scale='viridis')

    return br_fig


# QQ-Plot Callbacks
@callback(
    Output('QQ_plot', 'figure'),
    [Input('QQ_log_dropdown', 'value'),
     Input('tl_x_dropdown', 'value'),
     Input('tlx_slider', 'value'),
     Input('tl_y_dropdown', 'value'),
     Input('tly_slider', 'value'),
     Input('bl_x_dropdown', 'value'),
     Input('blx_slider', 'value'),
     Input('bl_y_dropdown', 'value'),
     Input('bly_slider', 'value'),
     Input('br_x_dropdown', 'value'),
     Input('brx_slider', 'value'),
     Input('br_y_dropdown', 'value'),
     Input('bry_slider', 'value'),
     Input('filepath', 'value'),
     Input('memory', 'data')
     ])

def update_QQ(log, ax_value, ax_range, ay_value, ay_range, bx_value, bx_range, by_value, by_range, cx_value, cx_range,
              cy_value, cy_range, filepath, data):

    df = pd.read_json(data, orient='split')
    quantiles = list(get_quantiles(filepath))

    ax_low, ax_high = ax_range
    ay_low, ay_high = ay_range
    bx_low, bx_high = bx_range
    by_low, by_high = by_range
    cx_low, cx_high = cx_range
    cy_low, cy_high = cy_range

    mask = (df[df[ax_value].between(ax_low, ax_high) & df[ay_value].between(ay_low, ay_high) &
               df[bx_value].between(bx_low, bx_high) & df[by_value].between(by_low, by_high) &
               df[cx_value].between(cx_low, cx_high) & df[cy_value].between(cy_low, cy_high)])

    QQ_plot = go.Figure()

    QQ_plot.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                                 y=quantiles, name = 'Observed',
                                 marker_color='rgba(0,0,0,0.5)'))
    QQ_plot.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                                 y=quantiles,
                                 marker_color='rgba(0,0,0,0.5)', showlegend=False))

    for idx, row in mask.iterrows():
        QQ_plot.add_trace(
            go.Scatter(
                x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                y=[row['Q1'], row['Q5'], row['Q10'], row['Q30'], row['Q50'], row['Q70'],
                   row['Q90'], row['Q95'], row['Q99']],
                mode="lines", showlegend=True, marker_color=trace_cols[idx % 8], name = idx
            )
        )

    if log == 'Log Axis: Yes':
        QQ_plot.update_yaxes(title='Flow (Log)', type="log")
    else:
        QQ_plot.update_yaxes()

    return QQ_plot
