# Chart Components for NYC Housing & Transportation Dashboard

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def create_housing_time_series(df: pd.DataFrame, boroughs=None) -> go.Figure:
    """RQ1: Affordable Housing Units by Borough & Year (Stacked Bar)"""
    if boroughs:
        df = df[df['borough'].isin(boroughs)]

    agg = df.groupby(['year', 'borough'])['total_affordable_units'].sum().reset_index()

    fig = px.bar(agg, x='year', y='total_affordable_units', color='borough',
                 title='Affordable Housing Units Completed by Borough & Year',
                 labels={'year': 'Year', 'total_affordable_units': 'Units', 'borough': 'Borough'},
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(barmode='stack', xaxis={'type': 'category'}, hovermode='x unified')
    return fig


def create_housing_heatmap(df: pd.DataFrame, top_n=20) -> go.Figure:
    """RQ1: Heatmap - Top N ZIP Codes × Year"""
    zip_totals = df.groupby('zip_code')['total_affordable_units'].sum().sort_values(ascending=False)
    top_zips = zip_totals.head(top_n).index.tolist()

    pivot = df[df['zip_code'].isin(top_zips)].pivot_table(
        index='zip_code', columns='year', values='total_affordable_units', fill_value=0
    )

    fig = px.imshow(pivot, aspect='auto',
                    title=f'Top {top_n} ZIP Codes — Affordable Units by Year',
                    labels={'x': 'Year', 'y': 'ZIP Code', 'color': 'Units'},
                    color_continuous_scale='Blues', text_auto=True)
    fig.update_layout(height=max(400, top_n * 25))
    return fig


def create_traffic_time_series(df: pd.DataFrame, locations=None) -> go.Figure:
    """RQ3: Traffic Volume by Location & Year (Line)"""
    # Need raw traffic data with location detail
    # This uses aggregated data - show by borough instead
    if locations:
        df = df[df['location'].isin(locations)] if 'location' in df.columns else df

    agg = df.groupby(['year', 'borough'])['total_vehicle_volume'].sum().reset_index()

    fig = px.line(agg, x='year', y='total_vehicle_volume', color='borough', markers=True,
                  title='Annual Traffic Volume by Borough',
                  labels={'year': 'Year', 'total_vehicle_volume': 'Vehicle Volume', 'borough': 'Borough'})
    fig.update_xaxes(type='category')
    fig.update_layout(hovermode='x unified')
    return fig


def create_traffic_change_bar(df: pd.DataFrame) -> go.Figure:
    """RQ4: % Change in Traffic Volume by Location"""
    if 'location' not in df.columns:
        # Use borough-level
        pivot = df.pivot_table(index='borough', columns='year', values='total_vehicle_volume', fill_value=0)
    else:
        pivot = df.pivot_table(index='location', columns='year', values='total_vehicle_volume', fill_value=0)

    years = sorted([c for c in pivot.columns if isinstance(c, (int, float))])
    if len(years) < 2:
        return go.Figure().add_annotation(text="Need at least 2 years of data", x=0.5, y=0.5, showarrow=False)

    first_y, last_y = years[0], years[-1]
    pivot['pct_change'] = ((pivot[last_y] - pivot[first_y]) / pivot[first_y].replace(0, np.nan)) * 100
    change_df = pivot[['pct_change']].reset_index().sort_values('pct_change')
    index_col = 'location' if 'location' in change_df.columns else 'borough'

    fig = px.bar(change_df, x='pct_change', y=index_col, orientation='h',
                 title=f'Traffic Volume % Change ({first_y} → {last_y})',
                 labels={'pct_change': '% Change', index_col: 'Location'},
                 color='pct_change', color_continuous_scale='RdBu_r', color_continuous_midpoint=0)
    return fig


def create_cross_domain_scatter(df: pd.DataFrame) -> go.Figure:
    """RQ5: % Change Housing vs % Change Traffic by ZIP (Cross-domain)"""
    years = sorted(df['year'].unique())
    if len(years) < 2:
        return go.Figure().add_annotation(text="Need at least 2 years of data", x=0.5, y=0.5, showarrow=False)

    first_y, last_y = years[0], years[-1]

    pivot = df.pivot_table(index='zip_code', columns='year',
                           values=['total_affordable_units', 'total_vehicle_volume'], fill_value=0)
    pivot.columns = [f'{col[0]}_{col[1]}' for col in pivot.columns]

    h_first, h_last = f'total_affordable_units_{first_y}', f'total_affordable_units_{last_y}'
    t_first, t_last = f'total_vehicle_volume_{first_y}', f'total_vehicle_volume_{last_y}'

    changes = pd.DataFrame({
        'zip_code': pivot.index,
        'housing_pct': ((pivot[h_last] - pivot[h_first]) / pivot[h_first].replace(0, np.nan)) * 100,
        'traffic_pct': ((pivot[t_last] - pivot[t_first]) / pivot[t_first].replace(0, np.nan)) * 100,
    }).dropna()

    # Filter extreme values
    changes = changes[(changes['housing_pct'].abs() < 1000) & (changes['traffic_pct'].abs() < 1000)]

    fig = px.scatter(changes, x='housing_pct', y='traffic_pct', hover_data=['zip_code'],
                     title=f'% Change Affordable Housing vs Traffic Volume ({first_y}→{last_y}) by ZIP',
                     labels={'housing_pct': '% Change Affordable Units', 'traffic_pct': '% Change Traffic Volume'},
                     trendline='ols')
    fig.add_hline(y=0, line_dash='dash', line_color='gray')
    fig.add_vline(x=0, line_dash='dash', line_color='gray')
    return fig


def create_housing_traffic_scatter(df: pd.DataFrame) -> go.Figure:
    """Cross-domain: Housing Units vs Traffic Volume (Current Year)"""
    both = df[(df['total_affordable_units'] > 0) & (df['total_vehicle_volume'] > 0)]

    fig = px.scatter(both, x='total_vehicle_volume', y='total_affordable_units',
                     color='borough', size='project_count' if 'project_count' in both.columns else None,
                     hover_data=['zip_code', 'year'],
                     title='Affordable Housing Units vs Traffic Volume (ZIP × Year)',
                     labels={'total_vehicle_volume': 'Annual Vehicle Volume', 'total_affordable_units': 'Affordable Units'},
                     trendline='ols')
    return fig


def create_traffic_boxplot(df: pd.DataFrame) -> go.Figure:
    """RQ7: Traffic Volume in ZIPs With vs Without Affordable Housing"""
    plot_df = df.copy()
    plot_df['has_affordable_housing'] = plot_df['total_affordable_units'] > 0
    plot_df['housing_status'] = plot_df['has_affordable_housing'].map({True: 'Has New Affordable Housing', False: 'No New Affordable Housing'})

    fig = px.box(plot_df, x='housing_status', y='total_vehicle_volume', color='housing_status',
                 title='Traffic Volume in ZIPs With vs Without New Affordable Housing',
                 labels={'housing_status': '', 'total_vehicle_volume': 'Annual Vehicle Volume'})
    return fig


def create_quadrant_chart(df: pd.DataFrame, year=None) -> go.Figure:
    """RQ8: Quadrant Chart - Housing vs Traffic by ZIP"""
    if year is None:
        year = df['year'].max()

    latest = df[df['year'] == year].copy()
    latest = latest[(latest['total_affordable_units'] > 0) | (latest['total_vehicle_volume'] > 0)]

    if len(latest) == 0:
        return go.Figure().add_annotation(text=f"No data for year {year}", x=0.5, y=0.5, showarrow=False)

    h_median = latest['total_affordable_units'].median()
    t_median = latest['total_vehicle_volume'].median()

    def quadrant(row):
        if row['total_affordable_units'] >= h_median and row['total_vehicle_volume'] >= t_median:
            return 'High Housing / High Traffic'
        elif row['total_affordable_units'] >= h_median and row['total_vehicle_volume'] < t_median:
            return 'High Housing / Low Traffic ⚠️'
        elif row['total_affordable_units'] < h_median and row['total_vehicle_volume'] >= t_median:
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

    fig = px.scatter(latest, x='total_vehicle_volume', y='total_affordable_units',
                     color='quadrant', hover_data=['zip_code', 'borough'],
                     title=f'Affordable Housing vs Traffic Volume by ZIP ({year}) — Quadrant Analysis',
                     labels={'total_vehicle_volume': 'Traffic Volume', 'total_affordable_units': 'Affordable Units'},
                     color_discrete_map=color_map)
    fig.add_hline(y=h_median, line_dash='dash', line_color='gray')
    fig.add_vline(x=t_median, line_dash='dash', line_color='gray')
    return fig


def create_time_series_facet(df: pd.DataFrame) -> go.Figure:
    """Faceted time series: Housing & Traffic by Borough"""
    ts = df.groupby(['year', 'borough']).agg({
        'total_affordable_units': 'sum',
        'total_vehicle_volume': 'sum'
    }).reset_index()

    fig = px.line(ts, x='year', y=['total_affordable_units', 'total_vehicle_volume'],
                  color='borough', facet_col='borough', facet_col_wrap=2,
                  title='Housing & Traffic Trends by Borough',
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