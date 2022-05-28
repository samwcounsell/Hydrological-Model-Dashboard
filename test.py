import pandas as pd
import plotly.express as px

df = pd.read_csv('data/Feb_2020.csv')

x_options = ['Arable_CMax', 'Arable_Evap', 'Arable_VarDist''Grassland_CMax', 'Grassland_Evap', 'Grassland_VarDist',
             'Forestry_CMax', 'Forestry_Evap', 'Forestry_VarDist', 'Urban_CMax', 'Urban_Evap', 'Urban_FTCoeff',
             'Class_5_STCoeff', 'Class_5_SoilTension', 'Class_7_STCoeff', 'Class_7_GWCoeff', 'Class_7_SoilTension',
             'Class_1_FTCoeff', 'Class_5_FTCoeff', 'Class_7_FTCoeff']

y_options = ['NSE_full_range', 'LogNSE_full_range', 'MARE', 'LogMARE', 'RMSE', 'VolError(%)']
