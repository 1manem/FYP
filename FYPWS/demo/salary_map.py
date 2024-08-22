from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sidebar import sidebar

# Load the data
salaryMap = pd.read_csv("C:/Users/William/Documents/FYPWS/demo/salaryMap.csv")

# Filter data for dropdown options (assuming countries are in 'Country' column)
country_options = [{'label': country, 'value': country} for country in salaryMap['Country'].unique()]

# Projection options for the dropdown menu
projection_options = [
    {'label': 'Map View', 'value': 'natural earth'},
    {'label': 'Globe View', 'value': 'orthographic'}
]

def salary_map_layout():
    return html.Div([
        sidebar(),  # Include the sidebar
        html.Div([
            html.H2("Salary by Country World Map"),
            dcc.Dropdown(
                id='country-search-dropdown-salary',
                options=country_options,
                placeholder='Select a country',
                style={'width': '35%'}  
            ),
            dcc.Dropdown(
                id='projection-dropdown-salary',
                options=projection_options,
                placeholder='Select a projection type',
                value='natural earth',  # Default projection type
                style={'width': '35%', 'marginTop': '10px'}
            ),
            dcc.Graph(
                id='salary-map',
                style={'width': '80%', 'height': '800px'} 
            )
        ], style={'marginLeft': '-170px', 'width': 'calc(100% - 250px)'})  
    ], style={'display': 'flex'})

def register_callbacks(app):
    @app.callback(
        Output('salary-map', 'figure'),
        [Input('country-search-dropdown-salary', 'value'),
         Input('projection-dropdown-salary', 'value')]
    )
    def update_map(selected_country, selected_projection):
        if selected_country:
            filtered_df = salaryMap[salaryMap['Country'] == selected_country]
        else:
            filtered_df = salaryMap

        figSalaryDash = px.choropleth(
            filtered_df,
            locations='Country',
            locationmode='country names',
            color='Median Salary',
            hover_name='Country',
            hover_data={
                'Median Salary': True,
                'Average Salary': True,
                'Lowest Salary': True,
                'Highest Salary': True
            },
            color_continuous_scale=px.colors.sequential.Plasma,
            projection=selected_projection,  # Use the selected projection type
            title='Median Salary by Country'
        )
        
        figSalaryDash.update_layout(
            title={
                'text': 'Salary by Country',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            geo=dict(
                showframe=True,
                showcoastlines=True,
                coastlinecolor='black',
                projection_type=selected_projection,
                bgcolor='#f5ebe0'
            ),
            coloraxis_colorbar=dict(
                title='Salary',
                tickprefix='$',
                titlefont=dict(size=14),
                tickfont=dict(size=12)
            ),
            paper_bgcolor='#f5ebe0',
            plot_bgcolor='#f5ebe0',
            height=800,
            width=1600
        )
        
        # Add annotations only when a country is selected
        if selected_country:
            if not filtered_df.empty:
                country_info = filtered_df.iloc[0]
                annotation_text = (
                    f"<b>Country:</b> {country_info['Country']}<br>"
                    f"<b>Median Salary:</b> ${country_info['Median Salary']:,}<br>"
                    f"<b>Average Salary:</b> ${country_info['Average Salary']:,}<br>"
                    f"<b>Lowest Salary:</b> ${country_info['Lowest Salary']:,}<br>"
                    f"<b>Highest Salary:</b> ${country_info['Highest Salary']:,}"
                )
                figSalaryDash.add_annotation(
                    x=0.05,
                    y=0.05,
                    text=annotation_text,
                    showarrow=True,
                    arrowhead=1,
                    xref='paper',
                    yref='paper',
                    align='center',
                    font=dict(size=16, color="black"),
                    borderwidth=1
                )
            else:
                figSalaryDash.add_annotation(
                    x=0.1,
                    y=0.1,
                    text="No country found matching your search.",
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    align='center',
                    font=dict(size=16, color="black"),
                    borderwidth=1
                )

        return figSalaryDash
