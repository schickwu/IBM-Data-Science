# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

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
                                            {'label': 'All Sites', 'value': 'All Sites'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            
                                        ],
                                        value='All Sites',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_output_container(entered_site):
    #print(entered_site)
    filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
    #print('hjjjh',filtered_df.columns)
    if entered_site == 'All Sites':
        #print('123')

        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by launch sites')
        return fig#html.Div(className='chart-item', children=html.Div(dcc.Graph(fig)))
    else:
        #print(spacex_df)
        launch_df1 = spacex_df[spacex_df['Launch Site']==entered_site]
        launch_d = launch_df1.groupby('class').count().reset_index()
        #launch_d.set_column
        print(launch_df1,launch_d)
        fig2 = px.pie(launch_d, values='Launch Site', 
        names='class', 
        title='Total Success Launches for Launch Site '+entered_site)
        return fig2#html.Div(className='chart-item', children=html.Div(dcc.Graph(fig2)))
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_pie_chart(entered_site,payload_mass):
    filtered_df3 = spacex_df[(payload_mass[1]>=spacex_df['Payload Mass (kg)'])&(spacex_df['Payload Mass (kg)']>= payload_mass[0])]
    if entered_site == 'All Sites':
        #print(filtered_df3)
        fig3 = px.scatter(filtered_df3, x='Payload Mass (kg)',y='class',color="Booster Version Category", 
        title='Correlation between payload and success rate for all launch sites')
        return fig3
    else:
        filtered_df2 = filtered_df3[filtered_df3['Launch Site']==entered_site]
        fig4 = px.scatter(filtered_df2, x='Payload Mass (kg)',y='class' ,color="Booster Version Category",
        title='Correlation between payload and success rate for launch sites '+entered_site)
        return fig4
        # return the outcomes piechart for a selected site

# Run the app
if __name__ == '__main__':
    app.run_server()
