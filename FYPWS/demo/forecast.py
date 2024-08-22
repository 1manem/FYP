from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import itertools
from sidebar import sidebar

# Load the data
GDPdata = pd.read_csv("C:/Users/William/Documents/FYPWS/demo/GDPmap.csv")
filtered_data = GDPdata[(GDPdata['Year'] >= 1950) & (GDPdata['Year'] <= 2018)]

# Extract unique country names for the dropdown
country_options = [{'label': country, 'value': country} for country in filtered_data['Country'].unique()]

# Function to create the forecasting layout
def forecasting_layout():
    return html.Div([
        sidebar(),
        html.Div([
            html.H2("GDP per Capita Forecast"),
            html.Div([
                html.Label("Select Country:"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=country_options,
                    placeholder='Select a country',
                    style={'margin-right': '10px', 'width': '300px'}
                ),
                html.Button(id='submit-button', n_clicks=0, children='Submit'),
            ], style={'margin-bottom': '20px', 'display': 'flex'}),
            html.Div(id='forecast-output', style={'display': 'flex'})
        ], style={'margin-left': '-170px', 'padding': '20px', 'backgroundColor': '#f5ebe0'})
    ], style={'display': 'flex', 'backgroundColor': '#f5ebe0'})

# Function to register the callbacks for the forecasting page
def register_forecasting_callbacks(app):
    @app.callback(
        Output('forecast-output', 'children'),
        Input('submit-button', 'n_clicks'),
        State('country-dropdown', 'value')
    )
    def update_forecast(n_clicks, country):
        if not n_clicks or not country:
            return ''
        filtered_data = GDPdata[GDPdata['Country'] == country]
        filtered_data = filtered_data[(filtered_data['Year'] >= 1950) & (filtered_data['Year'] <= 2018)]
        
        if filtered_data.empty:
            return f"No data available for {country}."
        
        filtered_data = filtered_data[['Year', 'GDP per capita']]
        filtered_data = filtered_data[filtered_data['GDP per capita'] != 0]
        
        if filtered_data.empty:
            return f"No valid data available for {country} after filtering out zero values."
        
        filtered_data.set_index('Year', inplace=True)
        
        try:
            # Determine the best ARIMA model order based on AIC
            p = d = q = range(0, 3)
            pdq = list(itertools.product(p, d, q))
            aic_values = []

            for param in pdq:
                try:
                    model = sm.tsa.ARIMA(filtered_data, order=param)
                    results = model.fit()
                    aic_values.append((param, results.aic))
                except:
                    continue

            best_order = sorted(aic_values, key=lambda x: x[1])[0][0]
            model = sm.tsa.ARIMA(filtered_data, order=best_order)
            results = model.fit()
            forecast = results.get_forecast(steps=10).predicted_mean
            
            future_years = pd.DataFrame({
                'Year': range(filtered_data.index[-1] + 1, filtered_data.index[-1] + 11),
                'GDP per capita': forecast
            }).set_index('Year')
            
            # Plotting
            fig, ax = plt.subplots(figsize=(12, 8))
            filtered_data.plot(ax=ax, label='Historical', color='blue')
            future_years.plot(ax=ax, label='Forecast', linestyle='--', color='orange')
            ax.set_title(f'GDP per Capita Forecast for {country}', fontsize=16)
            ax.set_xlabel('Year')
            ax.set_ylabel('GDP per Capita')
            ax.legend()
            ax.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save plot to PNG and encode to base64
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            
            # Return the plot and forecasted data
            return html.Div([
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(image_base64)),
                ], style={'flex': '2'}),
                html.Div([
                    html.H4('Forecasted GDP per Capita:', style={'margin-bottom': '10px', 'font-size': '18px'}),
                    dcc.Markdown(future_years.to_markdown(index=True))
                ], style={'flex': '1', 'padding-left': '20px'})
            ], style={'display': 'flex', 'backgroundColor': '#f5ebe0'})
        except Exception as e:
            return f"An error occurred while fitting the model or forecasting: {e}"
