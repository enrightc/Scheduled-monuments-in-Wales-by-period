import pandas as pd
import plotly.express as px

# 1. load the data
# df = dataframe
df = pd.read_csv("scheduled_monuments_wales_centroids_cleaned.csv")

print("All unique Period values in CSV:")
print(sorted(df["Period"].dropna().unique()))

print("Sites per period:")
print(df["Period"].value_counts())

# Explicitly define chronological order of periods
period_order = [
    "Prehistoric",
    "Neolithic",
    "Bronze Age",
    "Iron Age",
    "Roman",
    "Early Medieval",
    "Medieval",
    "Post Medieval",
    "Victorian",
    "Industrial",
    "Modern"
]

# Remove rows where the Period is "Unknown"

# df["Period"]
# → selects the 'Period' column from the dataframe

# df["Period"] != "Unknown"
# → checks each row and returns True if the period is NOT "Unknown"
# → results in a series of True / False values (one per row)

# df[ ... ]
# → keeps only the rows where the condition is True
# → rows where the condition is False ("Unknown") are dropped
df = df[df["Period"] != "Unknown"]

# Apply chronological ordering to the Period column
# This prevents Plotly (and pandas) from sorting periods alphabetically

# pd.Categorical(...)
# → tells pandas to treat this column as a set of defined categories,
#   rather than free text strings

# df["Period"]
# → uses the existing values in the Period column as the input data

# categories=period_order
# → defines the ONLY allowed period values
# → also defines the order they should follow (earliest → latest)

# ordered=True
# → tells pandas that the order of these categories matters
# → allows correct chronological sorting instead of alphabetical sorting
df["Period"] = pd.Categorical(
    df["Period"],
    categories=period_order,
    ordered=True
)

# 2. create a map figure
fig = px.scatter_mapbox(
    df,
    lon="lon",
    lat="lat",
    hover_name="Name",
    hover_data=["SAMNumber", "SiteType", "Period"],
    animation_frame="Period",
    category_orders={"Period": period_order},
    zoom=7,
    center={"lat": 52.5, "lon": -3.8},
)

# Marker styling (size + outline)
fig.update_traces(
    marker=dict(size=6, opacity=0.85),
    hovertemplate="<b>%{hovertext}</b><br>"
              "SAMNumber: %{customdata[0]}<br>"
              "SiteType: %{customdata[1]}<br>"
              "Period: %{customdata[2]}<extra></extra>"
)

# Basemap + Layout
fig.update_layout(
    mapbox_style="carto-positron",  # good default, no token needed
    width=900,
    height=900,
    margin=dict(l=20, r=20, t=60, b=20),
    title=dict(text="Scheduled monuments in Wales by period", x=0.5, xanchor="center"),
)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(
                    label="Play",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 700, "redraw": True},      # how long each period stays on screen
                            "transition": {"duration": 500, "easing": "cubic-in-out"},  # the smooth fade/move between periods
                            "fromcurrent": True,
                            "mode": "immediate",
                        },
                    ],
                ),
                dict(
                    label="Pause",
                    method="animate",
                    args=[
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": True},
                            "transition": {"duration": 0},
                            "mode": "immediate",
                        },
                    ],
                ),
            ],
        )
    ]
)

# 4. show the map
fig.show() # Opens a new browser with interactive map.

# Display unique period values
# print(df["Period"].unique())

# print(df["SiteType"].unique())

fig.write_html("index.html")