# Filter Components for NYC Housing & Transportation Dashboard

from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd


def create_filters(df: pd.DataFrame) -> html.Div:
    """Create all filter dropdowns and search input."""

    # Extract unique values for dropdowns
    years = sorted(df['year'].dropna().unique())
    boroughs = sorted(df['borough'].dropna().unique())
    zip_codes = sorted(df['zip_code'].dropna().unique())

    return html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H3("NYC Housing & Transportation Dashboard", className="text-center mb-3"),
                html.P("Explore the relationship between affordable housing development and traffic patterns",
                       className="text-center text-muted mb-4"),
            ])
        ]),

        # Filter Row 1: Borough, Year
        dbc.Row([
            dbc.Col([
                html.Label("Borough", className="fw-bold"),
                dcc.Dropdown(
                    id='filter-borough',
                    options=[{'label': b, 'value': b} for b in boroughs],
                    value=[],
                    multi=True,
                    placeholder="Select borough(s)...",
                    className="mb-3"
                ),
            ], md=4),

            dbc.Col([
                html.Label("Year", className="fw-bold"),
                dcc.Dropdown(
                    id='filter-year',
                    options=[{'label': str(y), 'value': int(y)} for y in years],
                    value=[],
                    multi=True,
                    placeholder="Select year(s)...",
                    className="mb-3"
                ),
            ], md=4),

            dbc.Col([
                html.Label("ZIP Code", className="fw-bold"),
                dcc.Dropdown(
                    id='filter-zip',
                    options=[{'label': z, 'value': z} for z in zip_codes],
                    value=[],
                    multi=True,
                    placeholder="Select ZIP code(s)...",
                    className="mb-3"
                ),
            ], md=4),
        ]),

        # Filter Row 2: Housing & Traffic categories
        dbc.Row([
            dbc.Col([
                html.Label("Housing Metric", className="fw-bold"),
                dcc.Dropdown(
                    id='filter-housing-metric',
                    options=[
                        {'label': 'Total Affordable Units', 'value': 'total_affordable_units'},
                        {'label': 'Total Units', 'value': 'total_units'},
                        {'label': 'Project Count', 'value': 'project_count'},
                        {'label': 'Building Count', 'value': 'building_count'},
                    ],
                    value='total_affordable_units',
                    clearable=False,
                    className="mb-3"
                ),
            ], md=6),

            dbc.Col([
                html.Label("Traffic Metric", className="fw-bold"),
                dcc.Dropdown(
                    id='filter-traffic-metric',
                    options=[
                        {'label': 'Total Vehicle Volume', 'value': 'total_vehicle_volume'},
                        {'label': 'Towards Manhattan', 'value': 'towards_manhattan'},
                        {'label': 'Towards Brooklyn', 'value': 'towards_brooklyn'},
                        {'label': 'Total Pedestrians', 'value': 'total_pedestrians'},
                    ],
                    value='total_vehicle_volume',
                    clearable=False,
                    className="mb-3"
                ),
            ], md=6),
        ]),

        # Search Mode
        dbc.Row([
            dbc.Col([
                html.Label("Search (natural language)", className="fw-bold"),
                dbc.InputGroup([
                    dbc.Input(
                        id='search-input',
                        type='text',
                        placeholder='e.g., "Brooklyn 2022 affordable housing" or "ZIP 11211 traffic"',
                        className="mb-3"
                    ),
                    dbc.Button("Search", id="search-btn", color="primary", className="mb-3"),
                ]),
            ], md=8),

            dbc.Col([
                html.Label(" ", className="fw-bold"),  # spacer
                dbc.Button(
                    "Generate Report",
                    id="generate-report-btn",
                    color="success",
                    size="lg",
                    className="w-100 mb-3",
                    style={"fontWeight": "bold", "fontSize": "1.1rem"}
                ),
            ], md=4),
        ]),

        # Active filters display
        html.Div(id='active-filters-display', className="mb-3"),

        html.Hr(),
    ])


def parse_search_query(query: str, df: pd.DataFrame) -> dict:
    """Parse natural language search query into filter dict."""
    if not query:
        return {}

    query_lower = query.lower()
    filters = {}

    # Extract borough
    boroughs = df['borough'].dropna().unique()
    for b in boroughs:
        if b.lower() in query_lower:
            filters['borough'] = [b]
            break

    # Extract year
    import re
    year_match = re.search(r'\b(20\d{2})\b', query)
    if year_match:
        filters['year'] = [int(year_match.group(1))]

    # Extract ZIP code
    zip_match = re.search(r'\b(\d{5})\b', query)
    if zip_match:
        filters['zip_code'] = [zip_match.group(1)]

    # Extract keywords
    if 'affordable' in query_lower or 'housing' in query_lower:
        filters['focus'] = 'housing'
    elif 'traffic' in query_lower or 'volume' in query_lower:
        filters['focus'] = 'traffic'

    return filters