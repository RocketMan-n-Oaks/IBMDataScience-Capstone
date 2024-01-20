# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px

def text_to_num(string):
    if string == 'Success':
        return 1
    elif string == 'Failure':
        return 0

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df = spacex_df.replace({'class':{0:'Failure', 1:'Success'}})
spacex_df['class_num'] = spacex_df['class'].apply(text_to_num)
max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label':'All Sites', 'value':'All'},
                                                 {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                 {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                 {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                 {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                             ],
                                             value='All',
                                             placeholder='Select a Launch Site',
                                             searchable=True,
                                             multi=False
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min_payload, max_payload, value=[min_payload, max_payload], id='payload-slider'),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))

def update_pie_chart(value):
    if value == 'All':
        # filtered_df = spacex_df.groupby('Launch_Site').count().reset_index()
        filtered_df = spacex_df.groupby('Launch_Site')['class_num'].sum().reset_index()
        fig = px.pie(filtered_df, values='class_num', names='Launch_Site', title='SpaceX Launches')
    else:
        filtered_df = spacex_df[spacex_df.Launch_Site == value].groupby(['class']).count().reset_index()
        fig = px.pie(filtered_df, values='Launch_Site', names='class', title='SpaceX Launch Success by Site',
                     color='class',
                     color_discrete_map={'Failure':"red", 'Success':"green"},
                     labels={'class': "Outcome"})

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@callback(
    Output('success-payload-scatter-chart','figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)

def update_scatter_plot(site, slider):
    if site == 'All':
        filtered_df = spacex_df
        filtered_df = filtered_df[filtered_df['PayloadMass'].between(slider[0], slider[1], inclusive='both')]
    else:
        filtered_df = spacex_df[spacex_df.Launch_Site == site]
        filtered_df = filtered_df[filtered_df['PayloadMass'].between(slider[0], slider[1], inclusive='both')]

    fig = px.scatter(filtered_df, x='Launch_Site', y='PayloadMass', color='class', labels={"class": "Outcome"},
                     color_discrete_map={'Failure':"red", 'Success':"green"})

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
