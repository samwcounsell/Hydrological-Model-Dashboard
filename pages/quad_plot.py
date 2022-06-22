from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob

from components.navbar import create_navbar
from functions.data_reading import pull_data

navbar = create_navbar()

df = pull_data('data')
types = 'text'

vars = list(df)

q = vars[-9:]
y_options = vars[-17:-9]
del (y_options[2:4])
x_options = vars[:-17]

min_val_tlx, min_val_tly, min_val_blx, min_val_bly, min_val_brx, min_val_bry = 0, -1, 0, -1, 0, -1
max_val_tlx, max_val_tly, max_val_blx, max_val_bly, max_val_brx, max_val_bry = 1000, 1000, 1000, 1000, 1000, 1000

trace_cols = ['seagreen', 'blue', 'cornflowerblue', 'lightgreen', 'forestgreen', 'gold', 'lightblue', 'lightgreen']

# Page layout
layout = html.Div([
    
    navbar,

    html.H1(
        children=' Kestrel-IHM 3-Dimensional Plot',
        style={'textAlign': 'center', 'padding': 30}
    ),

    # X, Y, Z       log
    dbc.Row([
        
        dbc.Col(dcc.Dropdown(id='tl_x_dropdown', options=x_options, value='Arable_CMax',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='tl_y_dropdown', options=y_options, value='VolError(%)',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='tl_z_dropdown', options=y_options, value='RMSE',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(html.P("")),
        dbc.Col(dcc.Dropdown(id='QQ_log_dropdown', options=['Yes', 'No'], value='No',
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

        dbc.Col(dcc.Dropdown(id='bl_x_dropdown', options=x_options, value='Forestry_CMax',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='bl_y_dropdown', options=y_options, value='VolError(%)',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='bl_z_dropdown', options=y_options, value='RMSE',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(html.P("")),
        dbc.Col(dcc.Dropdown(id='br_x_dropdown', options=x_options, value='Urban_CMax',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='br_y_dropdown', options=y_options, value='VolError(%)',
                         style={'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='br_z_dropdown', options=y_options, value='RMSE',
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
    
])



# Range Slider Updates
@callback(
    [Output('tlx_slider', 'min'),
     Output('tlx_slider', 'max')],
    Input('tl_x_dropdown', 'value'))
def update_TLXS(x_value):
    tlx_min_val = df[x_value].min()
    tlx_max_val = df[x_value].max()
    return tlx_min_val, tlx_max_val

@callback(
    [Output('tly_slider', 'min'),
     Output('tly_slider', 'max')],
    Input('tl_y_dropdown', 'value'))
def update_TLYS(y_value):
    tly_min_val = df[y_value].min()
    tly_max_val = df[y_value].max()
    return tly_min_val, tly_max_val

@callback(
    [Output('blx_slider', 'min'),
     Output('blx_slider', 'max')],
    Input('bl_x_dropdown', 'value'))
def update_BLXS(x_value):
    blx_min_val = df[x_value].min()
    blx_max_val = df[x_value].max()
    return blx_min_val, blx_max_val

@callback(
    [Output('bly_slider', 'min'),
     Output('bly_slider', 'max')],
    Input('bl_y_dropdown', 'value'))
def update_BLYS(y_value):
    bly_min_val = df[y_value].min()
    bly_max_val = df[y_value].max()
    return bly_min_val, bly_max_val


@callback(
    [Output('brx_slider', 'min'),
     Output('brx_slider', 'max')],
    Input('br_x_dropdown', 'value'))
def update_BRXS(x_value):
    brx_min_val = df[x_value].min()
    brx_max_val = df[x_value].max()
    return brx_min_val, brx_max_val

@callback(
    [Output('bry_slider', 'min'),
     Output('bry_slider', 'max')],
    Input('br_y_dropdown', 'value'))
def update_BRYS(y_value):
    bry_min_val = df[y_value].min()
    bry_max_val = df[y_value].max()
    return bry_min_val, bry_max_val

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
     Input('filepath', 'value')
     ])

# Function to create and update map depending on stage selected
def update_tl_fig(mainx_value, mainy_value, mainz_value, mainx_range, mainy_range, bx_value, by_value, bz_value, bx_range, by_range, cx_value, cy_value, cz_value, cx_range, cy_range, filepath):

    df = pull_data(filepath)

    mainx_low, mainx_high = mainx_range
    mainy_low, mainy_high = mainy_range
    bx_low, bx_high = bx_range
    by_low, by_high = by_range
    cx_low, cx_high = cx_range
    cy_low, cy_high = cy_range
    
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
     Input('filepath', 'value')
     ])

# Function to create and update map depending on stage selected
def update_bl_fig(mainx_value, mainy_value, mainz_value, mainx_range, mainy_range, bx_value, by_value, bz_value,
                  bx_range, by_range, cx_value, cy_value, cz_value, cx_range, cy_range, filepath):

    df = pull_data(filepath)
    
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
     Input('filepath', 'value')
     ])

# Function to create and update map depending on stage selected
def update_br_fig(mainx_value, mainy_value, mainz_value, mainx_range, mainy_range, bx_value, by_value, bz_value,
                  bx_range, by_range, cx_value, cy_value, cz_value, cx_range, cy_range, filepath):

    df = pull_data(filepath)

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
     Input('filepath', 'value')
     ])

def update_QQ(log, ax_value, ax_range, ay_value, ay_range, bx_value, bx_range, by_value, by_range, cx_value, cx_range,
              cy_value, cy_range, filepath):

    df = pull_data(filepath)

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
                                 y=[10.177, 4.72, 2.65, 0.995, 0.614, 0.412, 0.258, 0.217, 0.175], name="Observed",
                                 marker_color='rgba(0,0,0,0.5)'))
    QQ_plot.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                                 y=[10.177, 4.72, 2.65, 0.995, 0.614, 0.412, 0.258, 0.217, 0.175],
                                 marker_color='rgba(0,0,0,0.5)', showlegend=False))

    for idx, row in mask.iterrows():
        QQ_plot.add_trace(
            go.Scatter(
                x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                y=[row['Q1'], row['Q5'], row['Q10'], row['Q30'], row['Q50'], row['Q70'],
                   row['Q90'], row['Q95'], row['Q99']],
                mode="lines", showlegend=True, marker_color=trace_cols[idx % 8]
            )
        )

    if log == 'Yes':
        QQ_plot.update_yaxes(title='Flow (Log)', type="log")
    else:
        QQ_plot.update_yaxes()

    return QQ_plot
