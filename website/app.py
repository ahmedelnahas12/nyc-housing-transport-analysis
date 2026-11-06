# NYC Housing & Transportation Dashboard - Main Dash Application

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from website.components.filters import create_filters
from website.components.charts import CHART_REGISTRY
from website.components.layout import create_layout
from website.callbacks.filter_callbacks import register_filter_callbacks
from website.callbacks.chart_callbacks import register_chart_callbacks
from website.callbacks.report_callbacks import register_report_callbacks


# --- Initialize Dash App ---
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="NYC Housing & Transportation Dashboard",
    update_title=None,
)

server = app.server  # For gunicorn/vercel deployment


# --- Load Data ---
def load_data():
    """Load integrated dataset for the dashboard."""
    try:
        df = pd.read_csv("../notebooks/integrated_data.csv", low_memory=False)
        # Ensure proper types
        df['year'] = df['year'].astype(int)
        df['zip_code'] = df['zip_code'].astype(str).str.zfill(5)
        print(f"Loaded data: {df.shape}")
        return df
    except FileNotFoundError:
        print("Warning: integrated_data.csv not found. Using empty DataFrame.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()


# Load data at startup
df_full = load_data()


# --- App Layout ---
app.layout = create_layout()


# --- Inject Filters into Layout ---
@app.callback(
    dash.Output('filters-container', 'children'),
    dash.Input('filters-container', 'id')
)
def inject_filters(_):
    """Inject filter components into layout."""
    return create_filters(df_full)


# --- Register All Callbacks ---
register_filter_callbacks(app, df_full)
register_chart_callbacks(app)
register_report_callbacks(app)


# --- Health Check Endpoint (for Vercel) ---
@server.route('/health')
def health():
    return {"status": "ok", "data_loaded": not df_full.empty, "rows": len(df_full)}


# --- Main ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)