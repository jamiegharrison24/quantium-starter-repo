"""
Dash app: Pink Morsel sales visualiser.
Answers: Were sales higher before or after the price increase on 15 January 2021?
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA_PATH = Path(__file__).parent / "data" / "output.csv"
PRICE_INCREASE_DATE = "2021-01-15"

# Load and prepare data: aggregate sales by date, sort by date
df_raw = pd.read_csv(DATA_PATH)
df_raw["Date"] = pd.to_datetime(df_raw["Date"])
daily = df_raw.groupby("Date", as_index=False)["Sales"].sum()
daily = daily.sort_values("Date").reset_index(drop=True)

# Line chart figure
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

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1(
            "Pink Morsel Sales Over Time",
            style={"textAlign": "center", "marginBottom": "1rem"},
        ),
        dcc.Graph(id="sales-chart", figure=fig),
    ],
    style={"fontFamily": "sans-serif", "padding": "1rem", "maxWidth": "900px", "margin": "0 auto"},
)

if __name__ == "__main__":
    app.run(debug=True)
