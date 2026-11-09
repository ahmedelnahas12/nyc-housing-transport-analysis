# Report & Story Callbacks for NYC Housing & Transportation Dashboard

from dash import Input, Output, State, callback, no_update, html
import pandas as pd
import plotly.graph_objects as go


def _get_geo_col(df: pd.DataFrame) -> str:
    """Get the geographic column name (borough or zip_code)."""
    if 'borough' in df.columns:
        return 'borough'
    elif 'zip_code' in df.columns:
        return 'zip_code'
    return None


def register_report_callbacks(app):
    """Register callbacks for story section and report generation."""

    @app.callback(
        Output('story-question', 'children'),
        Output('story-findings', 'children'),
        Output('story-limitations', 'children'),
        Output('story-impact', 'children'),
        Input('generate-report-btn', 'n_clicks'),
        State('filtered-data-store', 'data'),
        State('full-data-store', 'data'),
        prevent_initial_call=True
    )
    def update_story_section(n_clicks, filtered_json, full_json):
        """Update story section based on filtered data."""
        if n_clicks is None or n_clicks == 0:
            return no_update, no_update, no_update, no_update

        def safe_read_json(json_str):
            if not json_str: return pd.DataFrame()
            try:
                import io
                if isinstance(json_str, str) and json_str.startswith('{'):
                    return pd.read_json(io.StringIO(json_str), orient='split')
                return pd.DataFrame()
            except Exception:
                return pd.DataFrame()

        if filtered_json:
            dff = safe_read_json(filtered_json)
        elif full_json:
            dff = safe_read_json(full_json)
        else:
            return no_update, no_update, no_update, no_update

        # Research Question
        question = "How does affordable housing development relate to traffic patterns in NYC neighborhoods?"

        # Key Findings (dynamic based on data)
        findings = []
        if len(dff) > 0:
            geo_col = _get_geo_col(dff)
            traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in dff.columns else 'total_vehicle_volume'

            # Finding 1: Correlation
            both = dff[(dff['total_affordable_units'] > 0) & (dff[traffic_col] > 0)]
            if len(both) > 2:
                corr = both['total_affordable_units'].corr(both[traffic_col])
                findings.append(html.Li(f"Correlation between affordable units and traffic volume: {corr:.3f} ({'positive' if corr > 0 else 'negative'})"))

            # Finding 2: Top geography
            geo_housing = dff.groupby(geo_col)['total_affordable_units'].sum()
            if not geo_housing.empty:
                top_geo = geo_housing.idxmax()
                findings.append(html.Li(f"Area with most affordable housing: {top_geo} ({geo_housing.max():,.0f} units)"))

            # Finding 3: Traffic trend
            if 'year' in dff.columns:
                yearly_traffic = dff.groupby('year')[traffic_col].sum()
                if len(yearly_traffic) >= 2:
                    trend = "increasing" if yearly_traffic.iloc[-1] > yearly_traffic.iloc[0] else "decreasing"
                    findings.append(html.Li(f"Traffic volume trend: {trend} over {yearly_traffic.index.min()}–{yearly_traffic.index.max()}"))

            # Finding 4: Quadrant insight
            latest_year = dff['year'].max()
            latest = dff[dff['year'] == latest_year]
            concern = latest[(latest['total_affordable_units'] > latest['total_affordable_units'].median()) &
                           (latest[traffic_col] < latest[traffic_col].median())]
            if len(concern) > 0:
                findings.append(html.Li(f"{len(concern)} areas have high affordable housing but low traffic volume — potential transit access gaps"))

        if not findings:
            findings = [html.Li("Apply filters and click Generate Report to see findings")]

        # Limitations
        limitations = [
            html.Li("Traffic data limited to bridge crossings, not comprehensive street network"),
            html.Li("Correlation ≠ causation: both housing and traffic driven by population/economic growth"),
            html.Li("ZIP code aggregation may mask within-ZIP variation"),
            html.Li("Spatial join assigns bridge traffic to single ZIP; bridges span boundaries"),
            html.Li("Temporal alignment at yearly level loses seasonal patterns"),
        ]

        # Impact
        impact = [
            html.Li("City Planners: Identify neighborhoods where affordable housing outpaces transportation capacity"),
            html.Li("Transit Agencies: Anticipate demand growth in areas with new affordable units"),
            html.Li("Housing Advocates: Flag communities needing transit investment alongside housing"),
            html.Li("Policy Makers: Coordinate housing and transportation capital planning"),
        ]

        return question, findings, limitations, impact