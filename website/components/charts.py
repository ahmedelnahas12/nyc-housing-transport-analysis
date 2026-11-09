# Chart Components for NYC Housing & Transportation Dashboard

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def _get_geo_col(df: pd.DataFrame) -> str:
    """Get the geographic column name (borough or zip_code)."""
    if 'borough' in df.columns:
        return 'borough'
    elif 'zip_code' in df.columns:
        return 'zip_code'
    return None


def create_housing_time_series(df: pd.DataFrame, geo_values=None) -> go.Figure:
    """RQ1: Affordable Housing Units by Geography & Year (Stacked Bar)"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if geo_values:
        df = df[df[geo_col].isin(geo_values)]

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    agg = df.groupby(['year', geo_col])['total_affordable_units'].sum().reset_index()

    fig = px.bar(agg, x='year', y='total_affordable_units', color=geo_col,
                 title=f'Affordable Housing Units Completed by {geo_col.replace("_", " ").title()} & Year',
                 labels={'year': 'Year', 'total_affordable_units': 'Units', geo_col: geo_col.replace("_", " ").title()},
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(barmode='stack', xaxis={'type': 'category'}, hovermode='x unified')
    return fig


def create_housing_heatmap(df: pd.DataFrame, top_n=20) -> go.Figure:
    """RQ1: Heatmap - Affordable Units by Geography × Year"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    pivot = df.pivot_table(
        index=geo_col, columns='year', values='total_affordable_units', fill_value=0, aggfunc='sum'
    )

    if pivot.empty:
        return go.Figure().add_annotation(text="No data available for heatmap", x=0.5, y=0.5, showarrow=False)

    fig = px.imshow(pivot, aspect='auto',
                    title=f'Affordable Units by {geo_col.replace("_", " ").title()} & Year',
                    labels={'x': 'Year', 'y': geo_col.replace("_", " ").title(), 'color': 'Units'},
                    color_continuous_scale='Blues', text_auto=True)
    return fig


def create_traffic_time_series(df: pd.DataFrame, geo_values=None) -> go.Figure:
    """RQ3: Traffic Volume by Geography & Year (Line)"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if geo_values:
        df = df[df[geo_col].isin(geo_values)]

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    # Use avg_traffic_volume column
    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    agg = df.groupby(['year', geo_col])[traffic_col].sum().reset_index()

    fig = px.line(agg, x='year', y=traffic_col, color=geo_col, markers=True,
                  title=f'Annual Traffic Volume by {geo_col.replace("_", " ").title()}',
                  labels={'year': 'Year', traffic_col: 'Vehicle Volume', geo_col: geo_col.replace("_", " ").title()})
    fig.update_xaxes(type='category')
    fig.update_layout(hovermode='x unified')
    return fig


def create_traffic_change_bar(df: pd.DataFrame) -> go.Figure:
    """RQ4: % Change in Traffic Volume by Geography"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    pivot = df.pivot_table(index=geo_col, columns='year', values=traffic_col, fill_value=0, aggfunc='sum')

    years = sorted([c for c in pivot.columns if isinstance(c, (int, float, np.integer))])
    if len(years) < 2:
        return go.Figure().add_annotation(text="Need at least 2 years of data for trend", x=0.5, y=0.5, showarrow=False)

    first_y, last_y = years[0], years[-1]
    pivot['pct_change'] = ((pivot[last_y] - pivot[first_y]) / pivot[first_y].replace(0, np.nan)) * 100
    change_df = pivot[['pct_change']].reset_index().sort_values('pct_change')

    fig = px.bar(change_df, x='pct_change', y=geo_col, orientation='h',
                 title=f'Traffic Volume % Change ({first_y} → {last_y})',
                 labels={'pct_change': '% Change', geo_col: geo_col.replace("_", " ").title()},
                 color='pct_change', color_continuous_scale='RdBu_r', color_continuous_midpoint=0)
    return fig


def create_cross_domain_scatter(df: pd.DataFrame) -> go.Figure:
    """RQ5: % Change Housing vs % Change Traffic by Geography (Cross-domain)"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    years = sorted(df['year'].unique())
    if len(years) < 2:
        return go.Figure().add_annotation(text="Need at least 2 years of data for trend", x=0.5, y=0.5, showarrow=False)

    first_y, last_y = years[0], years[-1]

    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    pivot = df.pivot_table(index=geo_col, columns='year',
                           values=['total_affordable_units', traffic_col], fill_value=0, aggfunc='sum')
    pivot.columns = [f'{col[0]}_{col[1]}' for col in pivot.columns]

    h_first, h_last = f'total_affordable_units_{first_y}', f'total_affordable_units_{last_y}'
    t_first, t_last = f'{traffic_col}_{first_y}', f'{traffic_col}_{last_y}'

    changes = pd.DataFrame({
        geo_col: pivot.index,
        'housing_pct': ((pivot[h_last] - pivot[h_first]) / pivot[h_first].replace(0, np.nan)) * 100,
        'traffic_pct': ((pivot[t_last] - pivot[t_first]) / pivot[t_first].replace(0, np.nan)) * 100,
    }).dropna()

    fig = px.scatter(changes, x='housing_pct', y='traffic_pct', hover_data=[geo_col],
                     title=f'% Change Affordable Housing vs Traffic Volume ({first_y}→{last_y}) by {geo_col.replace("_", " ").title()}',
                     labels={'housing_pct': '% Change Affordable Units', 'traffic_pct': '% Change Traffic Volume'},
                     trendline='ols' if len(changes) > 1 else None)
    fig.add_hline(y=0, line_dash='dash', line_color='gray')
    fig.add_vline(x=0, line_dash='dash', line_color='gray')
    return fig


def create_housing_traffic_scatter(df: pd.DataFrame) -> go.Figure:
    """Cross-domain: Housing Units vs Traffic Volume (Current Year)"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    # Scatter using Geography x Year aggregated data
    fig = px.scatter(df, x=traffic_col, y='total_affordable_units',
                     color=geo_col,
                     hover_data=['year'],
                     title=f'Affordable Housing Units vs Traffic Volume ({geo_col.replace("_", " ").title()} × Year)',
                     labels={traffic_col: 'Annual Vehicle Volume', 'total_affordable_units': 'Affordable Units'},
                     trendline='ols' if len(df) > 1 else None)
    return fig


def create_traffic_boxplot(df: pd.DataFrame) -> go.Figure:
    """RQ7: Traffic Volume Distribution by Geography"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    fig = px.box(df, x=geo_col, y=traffic_col, color=geo_col,
                 title=f'Traffic Volume Distribution by {geo_col.replace("_", " ").title()}',
                 labels={geo_col: geo_col.replace("_", " ").title(), traffic_col: 'Annual Vehicle Volume'})
    return fig


def create_quadrant_chart(df: pd.DataFrame, year=None) -> go.Figure:
    """RQ8: Quadrant Chart - Housing vs Traffic by Geography"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    if year is None:
        year = df['year'].max()

    latest = df[df['year'] == year].copy()

    if len(latest) == 0:
        return go.Figure().add_annotation(text=f"No data for year {year}", x=0.5, y=0.5, showarrow=False)

    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    h_median = latest['total_affordable_units'].median()
    t_median = latest[traffic_col].median()

    def quadrant(row):
        if row['total_affordable_units'] >= h_median and row[traffic_col] >= t_median:
            return 'High Housing / High Traffic'
        elif row['total_affordable_units'] >= h_median and row[traffic_col] < t_median:
            return 'High Housing / Low Traffic ⚠️'
        elif row['total_affordable_units'] < h_median and row[traffic_col] >= t_median:
            return 'Low Housing / High Traffic'
        else:
            return 'Low Housing / Low Traffic'

    latest['quadrant'] = latest.apply(quadrant, axis=1)

    color_map = {
        'High Housing / Low Traffic ⚠️': 'red',
        'High Housing / High Traffic': 'green',
        'Low Housing / High Traffic': 'blue',
        'Low Housing / Low Traffic': 'gray'
    }

    fig = px.scatter(latest, x=traffic_col, y='total_affordable_units',
                     color='quadrant', hover_data=[geo_col],
                     title=f'Affordable Housing vs Traffic Volume by {geo_col.replace("_", " ").title()} ({year}) — Quadrant Analysis',
                     labels={traffic_col: 'Traffic Volume', 'total_affordable_units': 'Affordable Units'},
                     color_discrete_map=color_map)
    fig.add_hline(y=h_median, line_dash='dash', line_color='gray')
    fig.add_vline(x=t_median, line_dash='dash', line_color='gray')
    return fig


def create_time_series_facet(df: pd.DataFrame) -> go.Figure:
    """Faceted time series: Housing & Traffic by Geography"""
    geo_col = _get_geo_col(df)
    if geo_col is None:
        return go.Figure().add_annotation(text="No geographic column found", x=0.5, y=0.5, showarrow=False)

    if len(df) == 0:
        return go.Figure().add_annotation(text="No data for selected filters", x=0.5, y=0.5, showarrow=False)

    traffic_col = 'avg_traffic_volume' if 'avg_traffic_volume' in df.columns else 'total_vehicle_volume'

    ts = df.groupby(['year', geo_col]).agg({
        'total_affordable_units': 'sum',
        traffic_col: 'sum'
    }).reset_index()

    fig = px.line(ts, x='year', y=['total_affordable_units', traffic_col],
                  color=geo_col, facet_col=geo_col, facet_col_wrap=2,
                  title=f'Housing & Traffic Trends by {geo_col.replace("_", " ").title()}',
                  labels={'value': 'Count', 'year': 'Year', 'variable': 'Metric'})
    fig.update_xaxes(type='category')
    return fig


# Chart registry for dynamic loading
CHART_REGISTRY = {
    'housing_time_series': create_housing_time_series,
    'housing_heatmap': create_housing_heatmap,
    'traffic_time_series': create_traffic_time_series,
    'traffic_change_bar': create_traffic_change_bar,
    'cross_domain_scatter': create_cross_domain_scatter,
    'housing_traffic_scatter': create_housing_traffic_scatter,
    'traffic_boxplot': create_traffic_boxplot,
    'quadrant_chart': create_quadrant_chart,
    'time_series_facet': create_time_series_facet,
}


def get_chart(chart_name: str, df: pd.DataFrame, **kwargs) -> go.Figure:
    """Get chart by name from registry."""
    if chart_name in CHART_REGISTRY:
        return CHART_REGISTRY[chart_name](df, **kwargs)
    return go.Figure().add_annotation(text=f"Chart '{chart_name}' not found", x=0.5, y=0.5, showarrow=False)