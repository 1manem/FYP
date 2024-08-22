from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sidebar import sidebar

# Load the data
GDPMap = pd.read_csv("C:/Users/William/Documents/FYPWS/demo/GDPMap.csv")

# Filter data for years 1950 to 2018
filtered_data = GDPMap[(GDPMap['Year'] >= 1950) & (GDPMap['Year'] <= 2018)]

def gdp_map_layout():
    return html.Div([
        sidebar(),  # Include the sidebar
        html.Div([
            html.H2("GDP per Capita World Map"),
            dcc.Dropdown(
                id='country-search-dropdown',
                options=[{'label': country, 'value': country} for country in filtered_data['Country'].unique()],
                placeholder='Select a country',
                style={'width': '35%'}  # Make dropdown menu narrower
            ),
            dcc.Dropdown(
                id='projection-dropdown',
                options=[
                    {'label': 'Map View', 'value': 'natural earth'},
                    {'label': 'Globe View', 'value': 'orthographic'}
                ],
                placeholder='Select a projection type',
                value='natural earth',  # Default projection type
                style={'width': '35%', 'marginTop': '10px'}
            ),
            dcc.Graph(
                id='gdp-map',
                style={'width': '50%', 'height': '800px'}  # Make plot wider and taller
            )
        ], style={'marginLeft': '-170px', 'width': 'calc(100% - 250px)', 'backgroundColor': '#f5ebe0'})  
    ], style={'display': 'flex', 'backgroundColor': '#f5ebe0'})

def register_callbacks(app):
    @app.callback(
        Output('gdp-map', 'figure'),
        [Input('country-search-dropdown', 'value'),
         Input('projection-dropdown', 'value')]
    )
    def update_map(selected_country, selected_projection):
        # Create animated choropleth map
        if selected_country:
            filtered_country_data = filtered_data[filtered_data['Country'] == selected_country]
            figGDPDash = px.choropleth(
                filtered_country_data,  # Use the filtered dataset for animation
                locations='Code',  # Use 'Code' as the identifier for countries
                color='GDP per capita',
                animation_frame='Year',  # Animate over years
                hover_name='Country',  # Label countries on hover
                range_color=[filtered_country_data['GDP per capita'].min(), filtered_country_data['GDP per capita'].max()],  # Adjust color scale
                projection=selected_projection,  # Apply the selected projection type
                title=f'GDP per capita of {selected_country} (1950-2018)',
                labels={'GDP per capita': 'GDP per capita ($USD)'}
            )
        else:
            figGDPDash = px.choropleth(
                filtered_data,  # Use the full dataset for animation
                locations='Code',  # Use 'Code' as the identifier for countries
                color='GDP per capita',
                animation_frame='Year',  # Animate over years
                hover_name='Country',  # Label countries on hover
                range_color=[filtered_data['GDP per capita'].min(), filtered_data['GDP per capita'].max()],  # Adjust color scale
                projection=selected_projection,  # Apply the selected projection type
                title='GDP per capita by Country (1950-2018)',
                labels={'GDP per capita': 'GDP per capita ($USD)'}
            )
        
        # Update layout to match the example
        figGDPDash.update_layout(
            title={
                'text': 'GDP per capita by Country (1950-2018)',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            geo=dict(
                showframe=True,
                showcoastlines=True,
                coastlinecolor='black',
                projection_type=selected_projection,  # Apply the selected projection type
                bgcolor='#f5ebe0'
            ),
            coloraxis_colorbar=dict(
                title='GDP per capita',
                tickprefix='$',
                titlefont=dict(size=14),
                tickfont=dict(size=12)
            ),
            paper_bgcolor='#f5ebe0',
            plot_bgcolor='#f5ebe0',
            height=800,
            width=1600
        )

        return figGDPDash
