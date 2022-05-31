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

min_val_tl, min_val_bl, min_val_br = 0, 0, 0
max_val_tl, max_val_bl, max_val_br = 1000, 1000, 1000

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
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='tl_y_dropdown', options=y_options, value='VolError(%)',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='tl_z_dropdown', options=y_options, value='RMSE',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(html.P("")),
        dbc.Col(dcc.Dropdown(id='QQ_log_dropdown', options=['Yes', 'No'], value='No',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),

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

    # slider
    dbc.Row([

        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='tl_slider', min=min_val_tl, max=max_val_tl, value=[min_val_tl, max_val_tl])),
        dbc.Col(html.P("")),

        ], style={"display": "grid", "grid-template-columns": "5% 40% 55%"}),



    # X Y Z        X Y Z

    dbc.Row([

        dbc.Col(dcc.Dropdown(id='bl_x_dropdown', options=x_options, value='Arable_CMax',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='bl_y_dropdown', options=y_options, value='VolError(%)',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='bl_z_dropdown', options=y_options, value='RMSE',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(html.P("")),
        dbc.Col(dcc.Dropdown(id='br_x_dropdown', options=x_options, value='Arable_CMax',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='br_y_dropdown', options=y_options, value='VolError(%)',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'})),
        dbc.Col(dcc.Dropdown(id='br_z_dropdown', options=y_options, value='RMSE',
                         style={'width': 400, 'textAlign': 'center', 'font-size': 'x-small'}))

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
        dbc.Col(dcc.RangeSlider(id='bl_slider', min=min_val_bl, max=max_val_bl, value=[min_val_bl, max_val_bl])),
        dbc.Col(html.P("")),
        dbc.Col(dcc.RangeSlider(id='br_slider', min=min_val_br, max=max_val_br, value=[min_val_br, max_val_br]))

    ], style={"display": "grid", "grid-template-columns": "5% 40% 15% 40%"}),
    
])



# Range Slider Updates
@callback(
    [Output('tl_slider', 'min'),
     Output('tl_slider', 'max')],
    Input('tl_x_dropdown', 'value'))
def update_TLS(x_value):
    tl_min_val = df[x_value].min()
    tl_max_val = df[x_value].max()
    return tl_min_val, tl_max_val

@callback(
    [Output('bl_slider', 'min'),
     Output('bl_slider', 'max')],
    Input('bl_x_dropdown', 'value'))
def update_BLS(x_value):
    bl_min_val = df[x_value].min()
    bl_max_val = df[x_value].max()
    return bl_min_val, bl_max_val

@callback(
    [Output('br_slider', 'min'),
     Output('br_slider', 'max')],
    Input('br_x_dropdown', 'value'))
def update_BRS(x_value):
    br_min_val = df[x_value].min()
    br_max_val = df[x_value].max()
    return br_min_val, br_max_val


# Standard plot Callbacks

# TL
@callback(
    Output('tl_fig', 'figure'),
    [Input('tl_x_dropdown', 'value'),
     Input('tl_y_dropdown', 'value'),
     Input('tl_z_dropdown', 'value'),
     Input('tl_slider', 'value'),
     Input('bl_x_dropdown', 'value'),
     Input('bl_slider', 'value'),
     Input('br_x_dropdown', 'value'),
     Input('br_slider', 'value')
     ])
# Function to create and update map depending on stage selected
def update_tl_fig(main_x_value, main_y_value, main_z_value, main_range, b_x_value, b_range, c_x_value, c_range):

    main_low, main_high = main_range
    b_low, b_high = b_range
    c_low, c_high = c_range
    mask = (df[df[main_x_value].between(main_low, main_high) & df[b_x_value].between(b_low, b_high) &
               df[c_x_value].between(c_low, c_high)])

    tl_fig = px.scatter(mask, x=main_x_value, y=main_y_value, color=main_z_value, color_continuous_scale='viridis')

    return tl_fig

# BL
@callback(
    Output('bl_fig', 'figure'),
    [Input('bl_x_dropdown', 'value'),
     Input('bl_y_dropdown', 'value'),
     Input('bl_z_dropdown', 'value'),
     Input('bl_slider', 'value'),
     Input('tl_x_dropdown', 'value'),
     Input('tl_slider', 'value'),
     Input('br_x_dropdown', 'value'),
     Input('br_slider', 'value')
     ])
# Function to create and update map depending on stage selected
def update_bl_fig(main_x_value, main_y_value, main_z_value, main_range, b_x_value, b_range, c_x_value, c_range):

    main_low, main_high = main_range
    b_low, b_high = b_range
    c_low, c_high = c_range
    mask = (df[df[main_x_value].between(main_low, main_high) & df[b_x_value].between(b_low, b_high) &
               df[c_x_value].between(c_low, c_high)])

    bl_fig = px.scatter(mask, x=main_x_value, y=main_y_value, color=main_z_value, color_continuous_scale='viridis')

    return bl_fig

# BR
@callback(
    Output('br_fig', 'figure'),
    [Input('br_x_dropdown', 'value'),
     Input('br_y_dropdown', 'value'),
     Input('br_z_dropdown', 'value'),
     Input('br_slider', 'value'),
     Input('tl_x_dropdown', 'value'),
     Input('tl_slider', 'value'),
     Input('bl_x_dropdown', 'value'),
     Input('bl_slider', 'value')
     ])
# Function to create and update map depending on stage selected
def update_br_fig(main_x_value, main_y_value, main_z_value, main_range, b_x_value, b_range, c_x_value, c_range):

    main_low, main_high = main_range
    b_low, b_high = b_range
    c_low, c_high = c_range
    mask = (df[df[main_x_value].between(main_low, main_high) & df[b_x_value].between(b_low, b_high) &
               df[c_x_value].between(c_low, c_high)])

    br_fig = px.scatter(mask, x=main_x_value, y=main_y_value, color=main_z_value, color_continuous_scale='viridis')

    return br_fig


# QQ-Plot Callbacks
@callback(
    Output('QQ_plot', 'figure'),
    [Input('QQ_log_dropdown', 'value'),
     Input('tl_x_dropdown', 'value'),
     Input('tl_slider', 'value'),
     Input('bl_x_dropdown', 'value'),
     Input('bl_slider', 'value'),
     Input('br_x_dropdown', 'value'),
     Input('br_slider', 'value')
     ])
def update_QQ(log, a_x_value, a_range, b_x_value, b_range, c_x_value, c_range):

    a_low, a_high = a_range
    b_low, b_high = b_range
    c_low, c_high = c_range
    mask = (df[df[a_x_value].between(a_low, a_high) & df[b_x_value].between(b_low, b_high) &
            df[c_x_value].between(c_low, c_high)])

    QQ_plot = go.Figure()
    for idx, row in mask.iterrows():
        QQ_plot.add_trace(
            go.Scatter(
                x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                y=[row['Q1'], row['Q5'], row['Q10'], row['Q30'], row['Q50'], row['Q70'],
                   row['Q90'], row['Q95'], row['Q99']],
                mode="lines", showlegend=False, marker_color=trace_cols[idx % 8]
            )
        )
    QQ_plot.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                               y=[10.177, 4.72, 2.65, 0.995, 0.614, 0.412, 0.258, 0.217, 0.175], name="Observed",
                               marker_color='rgba(0,0,0,0.5)'))
    QQ_plot.add_trace(go.Scatter(x=[1, 5, 10, 30, 50, 70, 90, 95, 99],
                               y=[10.177, 4.72, 2.65, 0.995, 0.614, 0.412, 0.258, 0.217, 0.175],
                               marker_color='rgba(0,0,0,0.5)', showlegend=False))
    QQ_plot.update_layout(xaxis=dict(title='Quantile'), yaxis=dict(title='Flow'))

    if log == 'Yes':
        QQ_plot.update_yaxes(title='Flow (Log)', type="log")
    else:
        QQ_plot.update_yaxes()

    return QQ_plot
