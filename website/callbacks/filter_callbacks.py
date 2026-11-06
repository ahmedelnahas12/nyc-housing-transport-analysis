# Filter & Search Callbacks for NYC Housing & Transportation Dashboard

from dash import Input, Output, State, callback, no_update, html
import pandas as pd
import json

from website.components.filters import parse_search_query


def register_filter_callbacks(app, df: pd.DataFrame):
    """Register all filter and search callbacks."""

    @app.callback(
        Output('full-data-store', 'data'),
        Input('full-data-store', 'id'),  # dummy trigger on load
        prevent_initial_call=False
    )
    def load_full_data(_):
        """Store full dataset in browser memory."""
        return df.to_json(date_format='iso', orient='split')

    @app.callback(
        Output('filtered-data-store', 'data'),
        Output('active-filters-display', 'children'),
        Input('filter-borough', 'value'),
        Input('filter-year', 'value'),
        Input('search-btn', 'n_clicks'),
        State('search-input', 'value'),
        State('full-data-store', 'data'),
        prevent_initial_call=True
    )
    def apply_filters(boroughs, years, search_clicks, search_query, full_data_json):
        """Apply dropdown filters and search to data."""
        if full_data_json is None:
            return no_update, no_update

        import io
        dff = pd.read_json(io.StringIO(full_data_json), orient='split')

        # Apply dropdown filters
        if boroughs:
            dff = dff[dff['borough'].isin(boroughs)]
        if years:
            dff = dff[dff['year'].isin(years)]

        # Apply search query (overrides dropdowns if provided)
        search_filters = {}
        if search_query and search_clicks:
            search_filters = parse_search_query(search_query, df)
            if search_filters.get('borough'):
                dff = dff[dff['borough'].isin(search_filters['borough'])]
            if search_filters.get('year'):
                dff = dff[dff['year'].isin(search_filters['year'])]

        # Build active filters display
        filter_parts = []
        if boroughs or search_filters.get('borough'):
            b = boroughs or search_filters.get('borough', [])
            filter_parts.append(f"Borough: {', '.join(b)}")
        if years or search_filters.get('year'):
            y = years or search_filters.get('year', [])
            filter_parts.append(f"Year: {', '.join(str(v) for v in y)}")
        if search_query and search_clicks:
            filter_parts.append(f"Search: \"{search_query}\"")

        active_display = html.Div([
            html.Span("Active filters: ", className="fw-bold text-muted"),
            html.Span(" | ".join(filter_parts) if filter_parts else "None (showing all data)")
        ], className="text-muted small")

        # FIX: Ensure dff is not empty or if it is, return a valid empty JSON representation
        # Using a simple empty DataFrame with columns instead of dff
        if dff.empty:
            dff = pd.DataFrame(columns=dff.columns)

        return dff.to_json(date_format='iso', orient='split'), active_display

    @app.callback(
        Output('filter-borough', 'value'),
        Output('filter-year', 'value'),
        Input('search-btn', 'n_clicks'),
        State('search-input', 'value'),
        State('full-data-store', 'data'),
        prevent_initial_call=True
    )
    def sync_dropdowns_from_search(search_clicks, search_query, full_data_json):
        """Sync dropdown values from search query."""
        if not search_query or not search_clicks or full_data_json is None:
            return no_update, no_update

        import io
        search_filters = parse_search_query(search_query, pd.read_json(io.StringIO(full_data_json), orient='split'))

        borough_val = search_filters.get('borough', no_update)
        year_val = search_filters.get('year', no_update)

        return borough_val, year_val