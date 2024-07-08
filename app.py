# app.py

import subprocess
import sys
import importlib
import gc

def install_and_import(package, install_name=None):
    install_name = install_name or package
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
    finally:
        globals()[package] = importlib.import_module(package)

# List of required packages with their pip install names
required_packages = {
    "plotly": "plotly",
    "pandas": "pandas",
    "sklearn": "scikit-learn"  # Note: We are installing 'scikit-learn' but importing 'sklearn'
}

for package, install_name in required_packages.items():
    install_and_import(package, install_name)

# Now import the required modules
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# Import necessary components from your modules
from dash import Dash, html, dcc
import ct_data_extraction  # Import the data extraction module
import predictive_visualizations  # Import the predictive visualizations module
import simple_histogram_1  # Import the histogram1 module
import simple_scatterplot  # Import the scatterplot module
import simple_histogram_2  # Import the histogram2 module

# Extract data
df = ct_data_extraction.extract_data()

# Release unused memory
del ct_data_extraction
gc.collect()

app = Dash(__name__)

# Added for Render application
server = app.server

app.layout = html.Div([
    html.H1("Clinical Trials Dashboard"),
    
    # Predictive Section
    html.H2("Predictive Section"),
    html.Div([
        html.Div(dcc.Graph(figure=predictive_visualizations.cm_fig), className='graph-container'),
        html.Div(dcc.Graph(figure=predictive_visualizations.report_fig), className='graph-container'),
        html.Div(dcc.Graph(figure=predictive_visualizations.feature_fig), className='graph-container')
    ], className='row'),

    # Exploratory Section
    html.H2("Exploratory Section"),
    html.Div([
        html.Div(dcc.Graph(figure=simple_histogram_1.fig_hist1), className='graph-container'),
        html.Div(dcc.Graph(figure=simple_scatterplot.fig_scatter), className='graph-container'),
        html.Div(dcc.Graph(figure=simple_histogram_2.fig_hist2), className='graph-container')
    ], className='row')
])

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8080)

