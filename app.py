# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 15:08:10 2021

@author: maikel
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from pandas.tseries.offsets import *
import numpy as np
#import base64
#from preprocessing_covid import general_clean, europe_cleaning


##### DEFINING HELPER FUNCTIONS FOR PREPROCESSING #####

def general_clean(df):
    """
    Function for a basic cleaning of the raw dataframe
    """

    

    # Cleaning rows
    row_cleaner = [ 'Africa', 'Asia', 'Central African Republic', 
                    'World', 'Europe', 'Oceania', 'South America', 
                    'European Union', 'Anguilla', 'Bosnia and Herzegovina',
                    'Brunei', 'Chad', 'Comoros', 'Djibouti', 'Equatorial Guinea',
                    'Eritrea', 'Eswatini','Gabon', 'Greenland', 'Grenada',
                    'Lesotho', 'Malawi', 'Micronesia (country)', 'Saint Helena', 
                    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
                    'Seychelles', 'Turks and Caicos Islands' ]

    return df[ ~df.location.isin(row_cleaner) ]

def europe_cleaning(df, pop = 5000000):
    """
    Function for a cleaning in the european countries 
    """

    # Doing Basic cleaning:
    df = general_clean(df)

    # Filtering: 
    df = df[ df.continent == 'Europe']

    # Keeping values with no NaN values in gdp:
    df = df[ ~df.gdp_per_capita.isna() ]

    # Keeping population over 5Mill
    df = df[df.population >= pop]

    # Cleaning negative values
    df = df[df.new_cases >= 0]
    df = df[df.new_deaths >= 0]

    # --- Preparing exports ---

    # Cases historical
    dfc = df[['iso_code', 'location', 'date','new_cases', 'new_deaths', 'new_cases_per_million', 'new_deaths_per_million', 
            'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million', 
            'population','gdp_per_capita', 'human_development_index']]

    dfc = dfc.sort_values(by=['location', 'date'])

    # Vaccination:
    dfvac = df[~df.total_vaccinations.isna()]

    dfvac = dfvac[['iso_code', 'location', 'date', 'total_vaccinations', 'new_vaccinations', 
                'people_vaccinated_per_hundred', 'population','gdp_per_capita', 'human_development_index']]

    dfvac = dfvac.sort_values(by=['location', 'date'])

    return dfc, dfvac


# Importing Preprocessed Data

#dfh = pd.read_csv('Data/preprocessed_cases_country.csv')
#dfv = pd.read_csv('Data/preprocessed_vaccination_country.csv')

df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

dfh , dfv = europe_cleaning(df, pop = 5000000)

# Define selection

country_options = [
    dict(label=country, value=country)
    for country in dfh.location.unique()]

cases_metrics = [
    {'label': 'New Cases', 'value': 'new_cases'},
    {'label': 'New Deaths', 'value': 'new_deaths'},
    {'label': 'New Cases per Million', 'value': 'new_cases_per_million'},
    {'label': 'New Deaths per Million', 'value': 'new_deaths_per_million'}
]

cases_total_metrics = [
    {'label': 'Total Cases', 'value': 'total_cases'},
    {'label': 'Total Deaths', 'value': 'total_deaths'},
    {'label': 'Total Cases per Million', 'value': 'total_cases_per_million'},
    {'label': 'Total Deaths per Million', 'value': 'total_deaths_per_million'}
]

vacc_metrics = [
    {'label': 'Total Vaccinations', 'value': 'total_vaccinations'},
    {'label': 'People Vaccinated per Hundred', 'value': 'people_vaccinated_per_hundred'},
    {'label': 'New Vaccinations', 'value': 'new_vaccinations'}
]

vacc_total_metrics = [
    {'label': 'Total Vaccinations', 'value': 'total_vaccinations'},
    {'label': 'People Vaccinated per Hundred', 'value': 'people_vaccinated_per_hundred'}
]

time_tosee = [
    {'label': 'Daily', 'value': 'Daily'},
    {'label': 'Weekly', 'value': 'Weekly'},
    {'label': 'Monthly', 'value': 'Monthly'}
]

app = dash.Dash(__name__, external_stylesheets='')
server = app.server

app.layout = html.Div([

    html.H1('Covid cases and Vaccination trends'),

    # Header divission
    html.Div([

        html.Div([

            html.Img(src='https://www.novaims.unl.pt/images/logo.png', style={'width': '130px'}),

        ], style={'width': '10%'}, className='ims-image'),

        html.Div([

            html.H3('Dashboard with analytics of Covid-19 metrics and vaccination process in european countries with a population over 5M.'),

            html.H3('Since the begining of the Covid-19 pandemic, misinformation has spread like the virus, this is a small effort to steer some sense into the numbers and to understanding the reality of the pandemic for some countries.'),

            html.H2('Developed for the subject of Data Visualization in the Master\'s Program in Data Science and Advanced Analytics at NOVA IMS.'),

        ], style={'width': '90%'}, className='dashboard_description'),
    ], style={'display': 'flex'}),

    dcc.Tabs([

        dcc.Tab(label = 'Cases', value='Cases', children = [

            # Trend Line Options
            html.Div([
                
                html.Div([

                    html.H5('Select Countries:'),
                    dcc.Dropdown(
                            id='country_drop',
                            options=country_options,
                            value=['Portugal','Spain'],
                            multi=True,
                            clearable=False,
                            placeholder = 'Select Countries'
                    ),
                    
                    html.H5('Select Metric:'),
                    dcc.Dropdown(
                            id='cases_metrics_dropdown',
                            options=cases_metrics,
                            value='new_cases_per_million',
                            multi=False,
                            clearable=False,
                            placeholder = 'Select Metric'
                    ),            

                ], style={'width': '20%'}, className='slicerblack'),#, 'background-color': '#111111'

            # Trend Line graph
            html.Div([
                    dcc.Graph(id='country_hist_cases')

                ], style={'width': '80%'}, className='graphblack')
            ], style={'display': 'flex'}),

            #Line break

            # Animation Options
            html.Div([

                html.Div([
                    
                    html.Br(),
                    
                    html.H4('Select Metric for animation:'),# style={'color': 'white', 'fontSize': 12, 'marginBottom': 2, 'font-style': 'italic'}),
                    dcc.Dropdown(
                            id='cases_total_metrics_dropdown',
                            options=cases_total_metrics,
                            value='total_deaths',
                            multi=False,
                            clearable=False,
                            placeholder = 'Select Metric for animation'
                    ),
                    
                    html.H4('Select level of detail for animation:'),
                    dcc.Dropdown(
                            id='time_detail',
                            options=time_tosee,
                            value='Weekly',
                            multi=False,
                            clearable=False,
                            placeholder = 'Select Level of detail'
                    ),
                    

                ], style={'width': '20%'}, className='slicerwhite'),

            # Animated Graph
            html.Div([

                    dcc.Graph(id='country_animation')

                ], style={'width': '80%'}, className='graphwhite')
            ], style={'display': 'flex'}),
        ]),

        dcc.Tab(label = 'Vaccination', value='Vaccination', children = [
            
            # Vacc trend line options
            html.Div([
                
                html.Div([
                    
                    html.H5('Select Country:'),
                    dcc.Dropdown(
                            id='vacc_country_dropdown',
                            options=country_options,
                            value=['France', 'Spain'],
                            multi=True,
                            clearable=False,
                            placeholder = 'Select Country'
                    ),

                    html.H5('Select Metric:'),
                    dcc.Dropdown(
                            id='vacc_metrics_dropdown_trend',
                            options=vacc_metrics,
                            value='total_vaccinations',
                            multi=False,
                            clearable=False,
                            placeholder = 'Select Metric'
                    ),        

                ], style={'width': '20%'}, className='slicerblack'),

            # Trend Line for Vacc
            html.Div([
                    dcc.Graph(id='trend_country_hist_vacc')

                ], style={'width': '80%'}, className='graphblack')
            ], style={'display': 'flex'}),

            #Line break

            # Vacc Animation Options
            html.Div([
                
                html.Div([
                    
                    html.H4('Select Metric:'),
                    dcc.Dropdown(
                            id='vacc_metrics_dropdown',
                            options=vacc_total_metrics,
                            value='people_vaccinated_per_hundred',
                            multi=False,
                            clearable=False,
                            placeholder = 'Select Metric'
                    ),            

                ], style={'width': '20%'}, className='slicerwhite'),

            # Animation vacc
            html.Div([
                    dcc.Graph(id='animation_country_vacc')

                ], style={'width': '80%'}, className='graphwhite')
            ], style={'display': 'flex'}),

        ])
    ], id = 'cases-vaccination', value = 'Cases', className='tabsss'),

    html.Label(['Author: Maikel Sousa m20200735 | Data Source: ', html.A('Our World in Data', href='https://ourworldindata.org/coronavirus-source-data')], className='footer_link'),
])

@app.callback(
    Output(component_id='country_hist_cases', component_property='figure'),
    [Input(component_id='country_drop', component_property='value'),
     Input(component_id='cases_metrics_dropdown', component_property='value')]
)
def trendGraph(countries, metric):
    dfselect = dfh[ dfh.location.isin(countries) ]
    dfselect = dfselect[ ['date','location', metric] ]
    
    fig = px.line(dfselect, x=dfselect.date, y=dfselect[metric].rolling(7).mean(), color='location')
    fig.update_layout(template="plotly_dark")
    
    hlpstr = str(metric).replace("_"," ")
    hlpstr = hlpstr.capitalize()
    
    fig.update_layout(title= "7 days average of " + hlpstr,
                      xaxis_title = "Dates",
                      yaxis_title = hlpstr,
                      legend_title = "Countries",
                      
                      font=dict(
                          family="Lato",
                          size=12,
                          color="White"
                          )
                      )

    return fig

@app.callback(
    Output(component_id='country_animation', component_property='figure'),
    [Input(component_id='cases_total_metrics_dropdown', component_property='value'),
     Input(component_id='time_detail', component_property='value')]
)
def cases_animation(metric ,time_detail):
    
    df = dfh
    # Preprocessing:
    
    df['Month'] = df.date.apply(pd.to_datetime).dt.strftime('%b-%Y')
    
    # Monthly transformation for visual:
    if time_detail == 'Monthly':
        df = df.groupby(by=['location', 'Month']).max()

        df = df[['date', 'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million']].reset_index()
        
        df['date'] = df.date.apply(pd.to_datetime) + MonthEnd(0)

        df = df.sort_values(by=['location', 'date'])
    
    # Weekly Transformation for visual:
    if time_detail == 'Weekly':
        df['Week'] = df.date.apply(pd.to_datetime).dt.isocalendar().week
        
        df = df.groupby(by=['location', 'Week']).max()

        df = df[['date', 'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million']].reset_index()
        
        df['Month'] = df.date.apply(pd.to_datetime).dt.strftime('%b-%Y')
        
        df['date'] = df['date'].apply(pd.to_datetime) + Week(weekday=0)        

        df = df.sort_values(by=['location', 'date'])   
    
    # Creating Figure
    frames = []

    #Locations = df.location.unique()
    loopDates = sorted(df.date.unique())

    hlpstr = str(metric).replace("_"," ")
    hlpstr = hlpstr.capitalize()

    for day in loopDates:
        # Getting the values for each location that specific day
        metric_in_day = df[ df.date == day ][['location', metric, 'Month']]\
                        .set_index('location')\
                        .sort_values(by=metric, ascending = False)

        MONTH = metric_in_day['Month'][0]

        # appending the values on each day:
        frames.append(dict(data=dict(type='bar',
                                     x = metric_in_day.index,
                                     y = metric_in_day[metric],
                                     name = metric + ' at ' + MONTH,
                                    ),
                           layout = go.Layout(title_text = hlpstr + ' on ' + MONTH )
                          )
                    )


    # Buttons:
    fig_bar_layout = dict(title=dict(text = hlpstr + ' since the pandemic started: '),
                          yaxis=dict(title = hlpstr
                                    ),
                          updatemenus=[dict(type="buttons",
                                        buttons=[dict(label="Play",
                                                      method="animate",
                                                      args=[None])
                                                ]
                                           )
                                      ]
                        )

    # Initial Data
    df_ = df[ df.date == loopDates[0] ][['location', metric, 'Month']]\
            .set_index('location')\
            .sort_values(by=metric, ascending = False)

    initial_data = dict(type='bar', 
                        x = df_.index, 
                        y = df_[metric],
                        name = metric + ' at the ' + df_['Month'][0] )

    fig_bar = go.Figure(data = initial_data, layout = fig_bar_layout, frames=frames)

    return fig_bar

@app.callback(
    Output(component_id='trend_country_hist_vacc', component_property='figure'),
    [Input(component_id='vacc_country_dropdown', component_property='value'),
    Input(component_id='vacc_metrics_dropdown_trend', component_property='value')]
)
def vacc_trend(countries, metric):
    
    dfselect = dfv[ dfv.location.isin(countries) ]
    dfselect = dfselect[ ['date','location', metric] ]
    
    fig = px.line(dfselect, x=dfselect.date, y=dfselect[metric], color='location')
    fig.update_layout(template="plotly_dark")
    
    hlpstr = str(metric).replace("_"," ")
    hlpstr = hlpstr.capitalize()
    
    fig.update_layout(title= hlpstr + 'trends',
                      xaxis_title = "Dates",
                      yaxis_title = hlpstr,
                      legend_title = "Countries",
                      
                      font=dict(
                          family="Lato",
                          size=12,
                          color="White"
                          )
                      )

    return fig

@app.callback(
    Output(component_id='animation_country_vacc', component_property='figure'),
    [Input(component_id='vacc_metrics_dropdown', component_property='value')]
)
def vacc_animation(metric):
    
    df = dfv

    # Weekly Transformation

    df['Week'] = df.date.apply(pd.to_datetime).dt.isocalendar().week
    
    df = df.groupby(by=['location', 'Week']).max()

    df = df[['date', 'total_vaccinations', 'people_vaccinated_per_hundred']].reset_index()
    
    df['date'] = df['date'].apply(pd.to_datetime) + Week(weekday=0)
    
    df['Month'] = df['date'].dt.strftime('%b-%Y')        

    df = df.sort_values(by=['location', 'date'])
    
    # Creating Figure
    frames = []

    loopDates = sorted(df.date.unique())

    hlpstr = str(metric).replace("_"," ")
    hlpstr = hlpstr.capitalize()

    for day in loopDates:
        # Getting the values for each location that specific day
        metric_in_day = df[ df.date == day ][['location', metric, 'Month']]\
                        .set_index('location')\
                        .sort_values(by=metric, ascending = False)

        MONTH = metric_in_day['Month'][0]

        # appending the values on each day:
        frames.append(dict(data=dict(type='bar',
                                     x = metric_in_day.index,
                                     y = metric_in_day[metric],
                                     name = metric + ' at ' + MONTH
                                    ),
                           layout = go.Layout(title_text = hlpstr + ' on ' + MONTH)
                          )
                    )

    # First introduction to buttons
    fig_bar_layout = dict(title=dict(text = hlpstr ),
                          yaxis=dict(title = hlpstr ),
                          updatemenus=[dict(type="buttons",
                                        buttons=[dict(label="Play",
                                                      method="animate",
                                                      args=[None])
                                                ]
                                           )
                                      ]
                        )

    # Initial Data
    df_ = df[ df.date == loopDates[0] ][['location', metric, 'Month']]\
            .set_index('location')\
            .sort_values(by=metric, ascending = False)

    initial_data = dict(type='bar', 
                        x = df_.index, 
                        y = df_[metric],
                        name = metric + ' at the ' + df_['Month'][0] )

    fig_bar = go.Figure(data = initial_data, layout = fig_bar_layout, frames=frames)

    return fig_bar


if __name__ == '__main__':
    app.run_server(debug=True)