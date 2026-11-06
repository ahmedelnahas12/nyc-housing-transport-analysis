# Layout Components for NYC Housing & Transportation Dashboard

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout() -> html.Div:
    """Create the main app layout structure."""
    return html.Div([
        # Header
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("NYC Housing & Transportation Dashboard", className="text-center mb-2"),
                    html.P("Exploring the relationship between affordable housing development and traffic patterns",
                           className="text-center text-muted mb-4"),
                ])
            ]),
        ], fluid=True, className="py-4"),

        # Filters Section
        dbc.Container([
            html.Div(id='filters-container'),
        ], fluid=True, className="px-4"),

        # Charts Section
        dbc.Container([
            dbc.Row([
                # Left column: Housing charts
                dbc.Col([
                    html.H4("Housing Analysis", className="mb-3"),
                    dcc.Loading([
                        dcc.Graph(id='chart-housing-time-series', config={'displayModeBar': True}),
                    ]),
                    html.Br(),
                    dcc.Loading([
                        dcc.Graph(id='chart-housing-heatmap', config={'displayModeBar': True}),
                    ]),
                ], md=6),

                # Right column: Traffic charts
                dbc.Col([
                    html.H4("Transportation Analysis", className="mb-3"),
                    dcc.Loading([
                        dcc.Graph(id='chart-traffic-time-series', config={'displayModeBar': True}),
                    ]),
                    html.Br(),
                    dcc.Loading([
                        dcc.Graph(id='chart-traffic-change', config={'displayModeBar': True}),
                    ]),
                ], md=6),
            ], className="mb-4"),

            # Cross-domain charts row
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H4("Cross-Domain Analysis", className="mb-3"),
                    dcc.Loading([
                        dcc.Graph(id='chart-cross-scatter', config={'displayModeBar': True}),
                    ]),
                ], md=6),

                dbc.Col([
                    dcc.Loading([
                        dcc.Graph(id='chart-quadrant', config={'displayModeBar': True}),
                    ]),
                ], md=6),
            ], className="mb-4"),

            # Additional cross-domain charts
            dbc.Row([
                dbc.Col([
                    dcc.Loading([
                        dcc.Graph(id='chart-housing-traffic-scatter', config={'displayModeBar': True}),
                    ]),
                ], md=6),

                dbc.Col([
                    dcc.Loading([
                        dcc.Graph(id='chart-traffic-boxplot', config={'displayModeBar': True}),
                    ]),
                ], md=6),
            ], className="mb-4"),

            # Faceted time series
            dbc.Row([
                dbc.Col([
                    dcc.Loading([
                        dcc.Graph(id='chart-facet-timeseries', config={'displayModeBar': True}),
                    ]),
                ], md=12),
            ], className="mb-4"),
        ], fluid=True, className="px-4 pb-4"),

        # Story Section
        dbc.Container([
            html.Hr(),
            html.H3("Our Data Story", className="text-center mb-4"),
            dbc.Row([
                dbc.Col([
                    html.H5("Research Question"),
                    html.P(id='story-question', className="lead"),
                ], md=6),
                dbc.Col([
                    html.H5("Key Findings"),
                    html.Ul(id='story-findings', className="lead"),
                ], md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Limitations"),
                    html.Ul(id='story-limitations'),
                ], md=6),
                dbc.Col([
                    html.H5("Impact for NYC"),
                    html.Ul(id='story-impact'),
                ], md=6),
            ]),
        ], fluid=True, className="px-4 py-4"),

        # Footer
        dbc.Container([
            html.Hr(),
            html.P([
                "Data sources: ",
                html.A("NYC Affordable Housing Production", href="https://data.cityofnewyork.us/resource/hg8x-zxpr.csv", target="_blank"),
                " | ",
                html.A("NYC Traffic Volume Counts", href="https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=download", target="_blank"),
                " | ",
                html.A("GitHub Repository", href="https://github.com/ahmedelnahas12/nyc-housing-transport-analysis", target="_blank"),
            ], className="text-center text-muted small"),
        ], fluid=True, className="pb-4"),

        # Stores for data passing
        dcc.Store(id='filtered-data-store'),
        dcc.Store(id='full-data-store'),
    ])