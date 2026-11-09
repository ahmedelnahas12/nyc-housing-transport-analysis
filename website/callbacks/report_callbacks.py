# Report & Story Callbacks for NYC Housing & Transportation Dashboard

from dash import Input, Output, State, callback, no_update, html
import pandas as pd

from website.components.filters import dataframe_from_store, normalize_frame


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

        def read_store(payload):
            try:
                return normalize_frame(dataframe_from_store(payload))
            except Exception:
                return pd.DataFrame()

        filtered = read_store(filtered_json)
        full = read_store(full_json)
        dff = filtered if filtered_json else full
        if full_json is None and filtered_json is None:
            return no_update, no_update, no_update, no_update

        # Research Question
        question = "How does affordable housing development relate to traffic patterns in NYC neighborhoods?"

        # Key Findings (dynamic based on data)
        findings = []
        if len(dff) > 0:
            # Finding 1: Correlation
            both = dff[(dff['total_affordable_units'] > 0) & (dff['total_vehicle_volume'] > 0)]
            if len(both) > 2:
                corr = both['total_affordable_units'].corr(both['total_vehicle_volume'])
                findings.append(html.Li(f"Correlation between affordable units and traffic volume: {corr:.3f} ({'positive' if corr > 0 else 'negative'})"))

            # Finding 2: Top borough
            borough_housing = dff.groupby('borough')['total_affordable_units'].sum()
            if not borough_housing.empty:
                top_borough = borough_housing.idxmax()
                findings.append(html.Li(f"Borough with most affordable housing: {top_borough} ({borough_housing.max():,.0f} units)"))

            # Finding 3: Traffic trend
            if 'year' in dff.columns:
                yearly_traffic = dff.groupby('year')['total_vehicle_volume'].sum()
                if len(yearly_traffic) >= 2:
                    trend = "increasing" if yearly_traffic.iloc[-1] > yearly_traffic.iloc[0] else "decreasing"
                    findings.append(html.Li(f"Traffic volume trend: {trend} over {yearly_traffic.index.min()}–{yearly_traffic.index.max()}"))

            # Finding 4: Quadrant insight
            latest_year = dff['year'].max()
            latest = dff[dff['year'] == latest_year]
            concern = latest[(latest['total_affordable_units'] > latest['total_affordable_units'].median()) &
                           (latest['total_vehicle_volume'] < latest['total_vehicle_volume'].median())]
            if len(concern) > 0:
                findings.append(html.Li(f"{len(concern)} boroughs have high affordable housing but low traffic volume — potential transit access gaps"))

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