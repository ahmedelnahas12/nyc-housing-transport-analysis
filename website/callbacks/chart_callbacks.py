# Chart Update Callbacks for NYC Housing & Transportation Dashboard

from dash import Input, Output, State, callback, no_update
import pandas as pd
import plotly.graph_objects as go

from website.components.charts import get_chart
from website.components.filters import dataframe_from_store, normalize_frame


def register_chart_callbacks(app):
    """Register all chart update callbacks triggered by Generate Report button."""

    chart_outputs = [
        Output('chart-housing-time-series', 'figure'),
        Output('chart-housing-heatmap', 'figure'),
        Output('chart-traffic-time-series', 'figure'),
        Output('chart-traffic-change', 'figure'),
        Output('chart-cross-scatter', 'figure'),
        Output('chart-quadrant', 'figure'),
        Output('chart-housing-traffic-scatter', 'figure'),
        Output('chart-traffic-boxplot', 'figure'),
        Output('chart-facet-timeseries', 'figure'),
    ]

    chart_names = [
        'housing_time_series',
        'housing_heatmap',
        'traffic_time_series',
        'traffic_change_bar',
        'cross_domain_scatter',
        'quadrant_chart',
        'housing_traffic_scatter',
        'traffic_boxplot',
        'time_series_facet',
    ]

    @app.callback(
        chart_outputs,
        Input('generate-report-btn', 'n_clicks'),
        State('filtered-data-store', 'data'),
        State('full-data-store', 'data'),
        prevent_initial_call=True
    )
    def update_all_charts(n_clicks, filtered_json, full_json):
        """Generate all charts from filtered data (or full data if no filters)."""
        if n_clicks is None or n_clicks == 0:
            return [no_update] * len(chart_outputs)

        def read_store(payload):
            try:
                return normalize_frame(dataframe_from_store(payload))
            except Exception as e:
                print(f"Error parsing stored data: {e}")
                return pd.DataFrame()

        filtered = read_store(filtered_json)
        full = read_store(full_json)
        # An empty filtered store means "no filter has been applied yet", not "nothing matched".
        dff = filtered if filtered_json else full

        if dff.empty:
            empty_fig = lambda msg: go.Figure().add_annotation(
                text=msg, x=0.5, y=0.5, showarrow=False, font_size=16
            )
            message = "No data matches current filters" if len(full) else "No integrated data is loaded"
            return [empty_fig(message)] * len(chart_outputs)

        figures = []
        for chart_name in chart_names:
            try:
                fig = get_chart(chart_name, dff)
                figures.append(fig)
            except Exception as e:
                figures.append(go.Figure().add_annotation(
                    text=f"Error generating {chart_name}: {str(e)}", x=0.5, y=0.5, showarrow=False
                ))

        return figures


# Need to import go for empty figure
import plotly.graph_objects as go