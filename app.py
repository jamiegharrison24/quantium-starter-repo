"""
Dash app: Pink Morsel sales visualiser.
Answers: Were sales higher before or after the price increase on 15 January 2021?
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

DATA_PATH = Path(__file__).parent / "data" / "output.csv"
PRICE_INCREASE_DATE = "2021-01-15"

# Load data (keep full df with Region for callback)
df_raw = pd.read_csv(DATA_PATH)
df_raw["Date"] = pd.to_datetime(df_raw["Date"])

REGION_OPTIONS = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]


def make_sales_figure(region_value: str):
    """Filter by region, aggregate by date, build line chart with price-increase marker."""
    if region_value == "all":
        subset = df_raw
    else:
        subset = df_raw[df_raw["Region"] == region_value]
    daily = subset.groupby("Date", as_index=False)["Sales"].sum()
    daily = daily.sort_values("Date").reset_index(drop=True)

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        title="",
        labels={"Date": "Date", "Sales": "Total Sales ($)"},
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        shapes=[
            {
                "type": "line",
                "x0": PRICE_INCREASE_DATE,
                "x1": PRICE_INCREASE_DATE,
                "y0": 0,
                "y1": 1,
                "yref": "paper",
                "line": {"color": "gray", "dash": "dash"},
            }
        ],
        annotations=[
            {
                "x": PRICE_INCREASE_DATE,
                "y": 1,
                "yref": "paper",
                "text": "Price increase",
                "showarrow": False,
                "xanchor": "left",
            }
        ],
    )
    return fig


app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Pink Morsel Sales Over Time", className="chart-title"),
        html.Div(
            [
                html.Label("Filter by region:", className="region-filter-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=REGION_OPTIONS,
                    value="all",
                    className="region-filter",
                ),
            ],
            className="region-filter-wrapper",
        ),
        html.Div(dcc.Graph(id="sales-chart"), className="chart-wrapper"),
    ],
    className="app-container",
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region_value: str):
    return make_sales_figure(region_value or "all")


if __name__ == "__main__":
    app.run(debug=True)
