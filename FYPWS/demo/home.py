from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sidebar import sidebar

# Sample DataFrame with normalized data
data = pd.read_csv("C:/Users/William/Documents/FYPWS/demo/complete_data.csv")
df = pd.DataFrame(data)

def home_layout():
    return html.Div([
        sidebar(),
        html.Div([
            dbc.Row([
                dbc.Col(
                    style={'padding': '0'}
                ),
                dbc.Col([
                    html.Div([
                        html.Img(src="/assets/headernew.png", style={'width': '100%', 'margin': '10px auto', 'display': 'block', 'opacity': '1'}),
                        dcc.Dropdown(
                            id='metric-dropdown',
                            options=[
                                {'label': 'Median Salary', 'value': 'Normalized Median Salary'},
                                {'label': 'Inequality in Income', 'value': 'Normalized Inequality in Income'},
                                {'label': 'GDP per capita', 'value': 'Normalized GDP per capita'},
                                {'label': 'Intensity of Deprivation Urban', 'value': 'Normalized Intensity of Deprivation Urban'},
                                {'label': 'Intensity of Deprivation Rural', 'value': 'Normalized Intensity of Deprivation Rural'},
                                {'label': 'Poverty Index', 'value': 'Poverty Index'}
                            ],
                            value='Poverty Index',  # Default value
                            style={'width': '1600px', 'margin': '0 auto'}
                        ),
                        dcc.Graph(id='bar-plot', style={'width': '100%', 'height': '600px'})
                    ], style={'textAlign': 'center'})
                ], width=12),
            ], style={'padding': '0px', 'backgroundColor': '#f5ebe0', 'borderRadius': '10px', 'textAlign': 'center'})
        ], style={'marginLeft': '-150px', 'backgroundColor': '#f5ebe0'})  # Adjusting the left margin for the main content
    ], style={'display': 'flex', 'width': '100%', 'margin': '0', 'padding': '0', 'backgroundColor': '#f5ebe0'})

# Define the callback to update the graph based on the selected metric
def update_graph(selected_metric):  
    # Filter out countries where any of the columns have a value of 0
    non_zero_countries = df[(df['Median Salary'] > 0) & 
                            (df['Inequality in Income'] > 0) & 
                            (df['GDP per capita'] > 0) & 
                            (df['Intensity of Deprivation Urban'] > 0) & 
                            (df['Intensity of Deprivation Rural'] > 0) & 
                            (df['Poverty Index'] > 0)]
    
    # Sort by the selected metric and select top 10
    top_10_countries = non_zero_countries.sort_values(by=selected_metric, ascending=False).head(10)
    
    # Create the plot
    fig = px.bar(
        top_10_countries,
        x=selected_metric,
        y='Country',
        orientation='h',
        title=f'Top 10 Countries by Normalized {selected_metric}',
        labels={selected_metric: selected_metric, 'Country': 'Country'},
        color=selected_metric
    )
    fig.update_layout(
        yaxis=dict(autorange='reversed'),
        plot_bgcolor='#f5ebe0',  # Background color of the plot area
        paper_bgcolor='#f5ebe0',  # Background color of the entire figure
        font=dict(color='black')  # Text color (optional, to improve readability)
    )
    return fig
