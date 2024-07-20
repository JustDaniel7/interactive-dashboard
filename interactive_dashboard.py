import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Load data from CSV with encoding handling
def load_data():
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            df = pd.read_csv('/sales_data.csv', encoding=encoding)
            print(f"Successfully read the file with {encoding} encoding.")
            break
        except UnicodeDecodeError:
            print(f"Failed to read with {encoding} encoding, trying next...")
    else:
        raise ValueError("Failed to read the CSV file with any of the attempted encodings.")
    
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    df['MONTH'] = df['ORDERDATE'].dt.strftime('%b')
    df['YEAR'] = df['ORDERDATE'].dt.year
    df['SALES'] = df['QUANTITYORDERED'] * df['PRICEEACH']
    return df

# Load the data
df = load_data()
top_products = df.groupby('PRODUCTLINE')['SALES'].sum().nlargest(5).index.tolist()

# Create the Dash app
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/dash-app/')

server = app.server

# Define the app layout
app.layout = html.Div(
    className='bg-gray-100 min-h-screen p-4',
    children=[
        html.Nav(
            className='bg-gray-800 p-4 shadow-md mb-4',
            children=[
                html.A("Product Sales Dashboard", className="text-lg font-bold text-gray-100 mx-4")
            ]
        ),
        
        html.Div(
            className='container mx-auto grid grid-cols-1 md:grid-cols-2 gap-4',
            children=[
                html.Div(
                    className='md:col-span-2',
                    children=[
                        html.Div(
                            className='rounded-lg shadow-md bg-white p-4',
                            children=[
                                html.H2("Product Line Sales Distribution", className="text-lg font-semibold mb-2"),
                                dcc.Graph(id='product-sales-distribution-chart')
                            ]
                        )
                    ]
                ),
                
                html.Div(
                    className='rounded-lg shadow-md bg-white p-4',
                    children=[
                        html.H2("Top 5 Product Lines by Total Sales", className="text-lg font-semibold mb-2"),
                        dcc.Graph(id='top-products-chart')
                    ]
                ),
                
                html.Div(
                    className='rounded-lg shadow-md bg-white p-4',
                    children=[
                        html.Label("Select Product Line:", className="block text-sm font-medium text-gray-700 mb-1"),
                        dcc.Dropdown(
                            id='product-dropdown',
                            options=[{'label': product, 'value': product} for product in top_products],
                            value=top_products[0],
                            className='rounded-lg shadow-sm p-2 w-full'
                        )
                    ]
                ),
                
                html.Div(
                    className='rounded-lg shadow-md bg-white p-4',
                    children=[
                        html.H2("Price vs Sales", className="text-lg font-semibold mb-2"),
                        dcc.Graph(id='price-vs-sales-chart')
                    ]
                ),
                
                html.Div(
                    className='rounded-lg shadow-md bg-white p-4',
                    children=[
                        html.H2("Monthly Sales", className="text-lg font-semibold mb-2"),
                        dcc.Graph(id='monthly-sales-chart')
                    ]
                )
            ]
        )
    ]
)

# Callbacks
@app.callback(
    Output('top-products-chart', 'figure'),
    Input('product-dropdown', 'options')
)
def update_top_products_chart(options):
    top_products_df = df[df['PRODUCTLINE'].isin([opt['label'] for opt in options])].groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    fig = px.bar(top_products_df, x='PRODUCTLINE', y='SALES', title="Top 5 Product Lines by Total Sales")
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
    return fig

@app.callback(
    Output('monthly-sales-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_monthly_sales_chart(selected_product):
    product_df = df[df['PRODUCTLINE'] == selected_product].groupby(['YEAR', 'MONTH'])['SALES'].sum().reset_index()
    product_df['DATE'] = pd.to_datetime(product_df['YEAR'].astype(str) + ' ' + product_df['MONTH'], format='%Y %b')
    product_df = product_df.sort_values('DATE')
    fig = px.line(product_df, x='DATE', y='SALES', title=f"Monthly Sales for {selected_product}")
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
    return fig

@app.callback(
    Output('price-vs-sales-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_price_vs_sales_chart(selected_product):
    product_df = df[df['PRODUCTLINE'] == selected_product].groupby(['YEAR', 'MONTH']).agg({
        'SALES': 'sum',
        'PRICEEACH': 'mean'
    }).reset_index()
    product_df['DATE'] = pd.to_datetime(product_df['YEAR'].astype(str) + ' ' + product_df['MONTH'], format='%Y %b')
    product_df = product_df.sort_values('DATE')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=product_df['DATE'], y=product_df['SALES'], name='Sales', yaxis='y1'))
    fig.add_trace(go.Scatter(x=product_df['DATE'], y=product_df['PRICEEACH'], name='Avg Price', yaxis='y2'))
    fig.update_layout(
        title=f"Price vs Sales for {selected_product}",
        yaxis=dict(title='Sales'),
        yaxis2=dict(title='Avg Price', overlaying='y', side='right'),
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig

@app.callback(
    Output('product-sales-distribution-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_product_sales_distribution(selected_product):
    product_sales_distribution = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    fig = px.pie(product_sales_distribution, values='SALES', names='PRODUCTLINE', title=f'Sales Distribution for Product Lines')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
