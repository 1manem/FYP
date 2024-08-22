from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sidebar import sidebar

# Load the data
income_transformed = pd.read_csv("C:/Users/William/Documents/FYPWS/demo/incomeMap.csv")

# Filter data for years 2010 to 2021
filtered_data2 = income_transformed[(income_transformed['Year'] >= 2010) & (income_transformed['Year'] <= 2021)]

# Create the choropleth map
figIncome = px.choropleth(
    filtered_data2,
    locations='Code',  # Use 'Code' as the identifier for countries
    color='Value',
    animation_frame='Year',  # Animate over years
    hover_name='Country',  # Label countries on hover
    hover_data={
        'Human Development Groups': True,
        'HDI Rank (2021)': True,
        'Value': True,
        'Year': False  # Hide Year in hover as it's already shown in animation frame
    },
    range_color=[filtered_data2['Value'].min(), filtered_data2['Value'].max()],  # Adjust color scale
    projection='natural earth',
    title='Inequality in Income by Country (2010-2021)',
    labels={'Value': 'Inequality in Income'}
)

def income_map_layout():
    return html.Div([
        sidebar(),  # Include the sidebar
        html.Div([
            html.H2("Inequality in Income World Map"),
            dcc.Dropdown(
                id='country-search-dropdown-income',
                options=[{'label': country, 'value': country} for country in filtered_data2['Country'].unique()],
                placeholder='Select a country',
                style={'width': '35%'}  # Make dropdown menu narrower
            ),
            dcc.Dropdown(
                id='projection-dropdown-income',
                options=[
                    {'label': 'Map View', 'value': 'natural earth'},
                    {'label': 'Globe View', 'value': 'orthographic'}
                ],
                placeholder='Select a projection type',
                value='natural earth',  # Default projection type
                style={'width': '35%', 'marginTop': '10px'}
            ),
            dcc.Graph(
                id='income-map',
                figure=figIncome,  # Set the figure directly
                style={'width': '80%', 'height': '800px'}  # Make plot wider and taller
            )
        ], style={'marginLeft': '-170px', 'width': 'calc(100% - 250px)'})  # Adjusting the left margin and width for the main content
    ], style={'display': 'flex'})

def register_callbacks(app):
    @app.callback(
        Output('income-map', 'figure'),
        [Input('country-search-dropdown-income', 'value'),
         Input('projection-dropdown-income', 'value')]
    )
    def update_income_map(selected_country, selected_projection):
        # Create animated choropleth map
        if selected_country:
            filtered_country_data = filtered_data2[filtered_data2['Country'] == selected_country]
            figIncomeDash = px.choropleth(
                filtered_country_data,  # Use the filtered dataset for animation
                locations='Code',  # Use 'Code' as the identifier for countries
                color='Value',
                animation_frame='Year',  # Animate over years
                hover_name='Country',  # Label countries on hover
                hover_data={
                    'Human Development Groups': True,
                    'HDI Rank (2021)': True,
                    'Value': True,
                    'Year': False  # Hide Year in hover as it's already shown in animation frame
                },
                range_color=[filtered_country_data['Value'].min(), filtered_country_data['Value'].max()],  # Adjust color scale
                projection=selected_projection,  # Apply the selected projection type
                title=f'Inequality in Income of {selected_country} (2010-2021)',
                labels={'Value': 'Inequality in Income'}
            )
        else:
            figIncomeDash = px.choropleth(
                filtered_data2,  # Use the full dataset for animation
                locations='Code',  # Use 'Code' as the identifier for countries
                color='Value',
                animation_frame='Year',  # Animate over years
                hover_name='Country',  # Label countries on hover
                hover_data={
                    'Human Development Groups': True,
                    'HDI Rank (2021)': True,
                    'Value': True,
                    'Year': False  # Hide Year in hover as it's already shown in animation frame
                },
                range_color=[filtered_data2['Value'].min(), filtered_data2['Value'].max()],  # Adjust color scale
                projection=selected_projection,  # Apply the selected projection type
                title='Inequality in Income by Country (2010-2021)',
                labels={'Value': 'Inequality in Income'}
            )
        
        # Update layout to match the example
        figIncomeDash.update_layout(
            title={
                'text': 'Inequality in Income by Country (2010-2021)',
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
                title='Inequality in Income',
                tickprefix='%',
                titlefont=dict(size=14),
                tickfont=dict(size=12)
            ),
            paper_bgcolor='#f5ebe0',
            plot_bgcolor='#f5ebe0',
            height=800,
            width=1600
        )

        return figIncomeDash
