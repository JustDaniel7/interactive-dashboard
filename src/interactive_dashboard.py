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
            df = pd.read_csv('../dataset/sales_data.csv', encoding=encoding)
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

# Create the Dash app
app = dash.Dash(__name__)

# Load the data
df = load_data()

# Calculate top products
top_products = df.groupby('PRODUCTLINE')['SALES'].sum().nlargest(5).index.tolist()

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Product Sales Dashboard"),
    
    html.Div([
        html.H2("Top 5 Product Lines by Total Sales"),
        dcc.Graph(id='top-products-chart')
    ]),
    
    html.Div([
        html.Label("Select Product Line:"),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in top_products],
            value=top_products[0]
        )
    ]),
    
    html.Div([
        html.Div([
            html.H2("Monthly Sales"),
            dcc.Graph(id='monthly-sales-chart')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            html.H2("Price vs Sales"),
            dcc.Graph(id='price-vs-sales-chart')
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
])

# Callback for updating the top products chart
@app.callback(
    Output('top-products-chart', 'figure'),
    Input('product-dropdown', 'options')
)
def update_top_products_chart(options):
    top_products_df = df[df['PRODUCTLINE'].isin(top_products)].groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    fig = px.bar(top_products_df, x='PRODUCTLINE', y='SALES', title="Top 5 Product Lines by Total Sales")
    return fig

# Callback for updating the monthly sales chart
@app.callback(
    Output('monthly-sales-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_monthly_sales_chart(selected_product):
    product_df = df[df['PRODUCTLINE'] == selected_product].groupby(['YEAR', 'MONTH'])['SALES'].sum().reset_index()
    product_df['DATE'] = pd.to_datetime(product_df['YEAR'].astype(str) + ' ' + product_df['MONTH'], format='%Y %b')
    product_df = product_df.sort_values('DATE')
    fig = px.line(product_df, x='DATE', y='SALES', title=f"Monthly Sales for {selected_product}")
    return fig

# Callback for updating the price vs sales chart
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
        yaxis2=dict(title='Avg Price', overlaying='y', side='right')
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)