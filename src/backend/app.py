from flask import Flask, jsonify, request
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__)

# Load your dataset
housing_data = pd.read_csv('../../dataset/sales_data.csv')

@app.route('/')
def home():
    return "Housing Dashboard API"

@app.route('/api/price_distribution', methods=['GET'])
def price_distribution():
    fig = px.histogram(housing_data, x='median_house_value', nbins=50, title='Distribution of Housing Prices')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graph_json)

@app.route('/api/scatter_plot', methods=['GET'])
def scatter_plot():
    fig = px.scatter(housing_data, x='median_income', y='median_house_value', color='ocean_proximity',
                     title='Median Income vs. Median House Value')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)
