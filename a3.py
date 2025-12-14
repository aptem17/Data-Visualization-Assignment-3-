
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


DATA_PATH = r"D:\TCD Notes and assignments\Data Viz\Assgn2\Global_Mobile_Prices_2025_Extended.csv"
df = pd.read_csv(DATA_PATH)


# Preprocessing

month_map = {
    'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
    'july':7,'august':8,'september':9,'october':10,'november':11,'december':12
}

df["release_month_num"] = df["release_month"].str.lower().map(month_map)
df["month_year"] = df.apply(
    lambda r: f"{int(r['year'])}-{int(r['release_month_num']):02d}"
    if pd.notna(r["release_month_num"]) else None,
    axis=1
)

top_brands = df["brand"].value_counts().nlargest(6).index.tolist()
df["brand_top"] = df["brand"].apply(lambda x: x if x in top_brands else "Other")

num_cols = ["price_usd","ram_gb","camera_mp","battery_mah","rating"]


def price_segment(price):
    if price < 300:
        return "Budget"
    elif price < 700:
        return "Mid-range"
    else:
        return "Premium"

df["price_segment"] = df["price_usd"].apply(price_segment)


# App

app = Dash(__name__)
app.title = "Smartphone Market 2025"


# Layout

app.layout = html.Div([

    html.H2("Global Smartphone Market 2025 — Interactive Analysis",
            style={"textAlign":"center","marginBottom":"15px"}),

    html.Div([

        
        html.Div([
            html.H4("Filters"),

            dcc.Dropdown(
                id="brand-filter",
                options=[{"label":b,"value":b} for b in sorted(df["brand_top"].unique())],
                multi=True,
                placeholder="Brand"
            ),

            dcc.Dropdown(
                id="os-filter",
                options=[{"label":o,"value":o} for o in df["os"].unique()],
                multi=True,
                placeholder="Operating System"
            ),

            dcc.Checklist(
                id="filter-5g",
                options=[{"label":" Only 5G","value":"5g"}]
            ),

            html.Label("Price Range ($)"),
            dcc.RangeSlider(
                id="price-slider",
                min=df.price_usd.min(),
                max=df.price_usd.max(),
                value=[df.price_usd.min(), df.price_usd.max()],
                marks=None,
                tooltip={"always_visible":True}
            ),

            html.Label("Scatter Y"),
            dcc.Dropdown(
                id="scatter-y",
                options=[{"label":c.replace("_"," ").title(),"value":c} for c in num_cols],
                value="camera_mp"
            ),

            html.Label("Scatter Size"),
            dcc.Dropdown(
                id="scatter-size",
                options=[{"label":c.replace("_"," ").title(),"value":c} for c in num_cols],
                value="battery_mah"
            )

        ], style={
            "width":"20%",
            "padding":"15px",
            "border":"1px solid #ddd",
            "borderRadius":"8px"
        }),

        
        html.Div([
            html.H4("Quick Insights"),

            dcc.Graph(id="box-price", style={"height":"500px"}),
            dcc.Graph(id="corr-heatmap", style={"height":"500px"})

        ], style={
            "width":"35%",
            "padding":"10px"
        }),

        
        html.Div([

            dcc.Tabs(id="tabs", value="scatter", children=[
                dcc.Tab(label="Scatter & Multivariate", value="scatter"),
                dcc.Tab(label="Brand Facets", value="facet"),
                dcc.Tab(label="Temporal Graph", value="anim-tab")
            ]),

            html.Div(id="tab-content")

        ], style={
            "width":"55%",
            "padding":"10px"
        })

    ], style={"display":"flex","gap":"10px"}),


])


# Helper

def apply_filters(brands, oses, only5g, price_range):
    d = df.copy()
    if brands:
        d = d[d.brand_top.isin(brands)]
    if oses:
        d = d[d.os.isin(oses)]
    if only5g:
        d = d[d["5g_support"]=="Yes"]
    d = d[(d.price_usd>=price_range[0]) & (d.price_usd<=price_range[1])]
    return d

def add_price_segment(d):
    d = d.copy()
    d["price_segment"] = pd.cut(
        d["price_usd"],
        bins=[0, 400, 800, d["price_usd"].max() + 1],
        labels=["Budget", "Mid-range", "Premium"]
    )
    return d


# Main Tab Callback

@app.callback(
    Output("tab-content","children"),
    Input("tabs","value"),
    Input("brand-filter","value"),
    Input("os-filter","value"),
    Input("filter-5g","value"),
    Input("price-slider","value"),
    Input("scatter-y","value"),
    Input("scatter-size","value")
)
def update_tabs(tab, brands, oses, f5g, price, y, size):

    d = apply_filters(brands, oses, f5g, price)
    if d.empty:
        return html.H4("No data for selected filters")

    if tab=="scatter":
        fig1 = px.scatter(
            d, x="price_usd", y=y, size=size,
            color="brand_top",
            hover_data=["brand","model","rating"],
            height=500
        )

        fig2 = px.parallel_coordinates(
            d,
            dimensions=num_cols,
            color="price_usd",
            color_continuous_scale=px.colors.sequential.Viridis,
            height=500
        )

        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ])

    if tab=="facet":
        fig = px.scatter(
            d, x="price_usd", y="rating",
            facet_col="brand_top",
            facet_col_wrap=3,
            color="brand_top",
            height=900
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        return dcc.Graph(figure=fig)

    if tab == "anim-tab":

        if d["release_month_num"].isna().all():
            return html.H4("No valid monthly data available.")

        
        monthly = (
            d.groupby("release_month_num")
            .agg(avg_price=("price_usd", "mean"))
            .reset_index()
            .sort_values("release_month_num")
        )

        
        month_names = {
            1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
            7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
        }
        monthly["month"] = monthly["release_month_num"].map(month_names)

        fig_time = px.line(
            monthly,
            x="month",
            y="avg_price",
            markers=True,
            title="Average Smartphone Price by Release Month (2025)",
            height=700
        )

        fig_time.update_layout(
            xaxis_title="Release Month",
            yaxis_title="Average Price (USD)"
        )

        return dcc.Graph(figure=fig_time)


# Insights Callback

@app.callback(
    Output("box-price","figure"),
    Output("corr-heatmap","figure"),
    Input("brand-filter","value"),
    Input("os-filter","value"),
    Input("filter-5g","value"),
    Input("price-slider","value")
)
def update_insights(brands, oses, f5g, price):

    d = apply_filters(brands, oses, f5g, price)
    if d.empty:
        return {}, {}

    box = px.box(
        d, y="price_usd", color="brand_top",
        title="Price Distribution"
    )

    corr = d[num_cols].corr()
    heat = px.imshow(
        corr, text_auto=True,
        title="Attribute Correlations",
        aspect="auto"
    )

    return box, heat





if __name__ == "__main__":
    app.run(debug=True, port=8050)
