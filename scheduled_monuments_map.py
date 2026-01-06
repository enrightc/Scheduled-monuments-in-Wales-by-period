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
fig = px.scatter_geo(
    df,
    lon="lon",
    lat="lat",
    hover_name="Name",
    hover_data=["SAMNumber", "SiteType", "Period"],
    animation_frame="Period",
    category_orders={"Period": period_order},
)

# Marker styling (size + outline)
fig.update_traces(
    marker=dict(size=6, opacity=0.85, line=dict(width=0.5, color="white")),
    hovertemplate="<b>%{hovertext}</b><br>"
              "SAMNumber: %{customdata[0]}<br>"
              "SiteType: %{customdata[1]}<br>"
              "Period: %{customdata[2]}<extra></extra>"
)

# Page/layout sizing
fig.update_layout(
    width=1000,
    height=700,
    margin=dict(l=20, r=20, t=70, b=200),
    title=dict(
        text=(
            "Scheduled monuments in Wales by period<br>"
            "<span style='font-size:14px;color:#555;'>"
            "Each frame shows the spatial distribution of scheduled monuments recorded for that period"
            "</span>"
        ),
        x=0.5,
        xanchor="center"
    ),
    annotations=[
        dict(
            text=(
                "Designated Historic Asset GIS Data, The Welsh Historic Environment Service (Cadw), "
                "DATE [enter the date you received the data], licensed under the Open Government Licence v3.0.<br>"
                "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
            ),
            x=0.5,
            y=-0.35,
            xref="paper",
            yref="paper",
            xanchor="center",
            yanchor="top",
            showarrow=False,
            font=dict(size=10, color="#555"),
            align="center",
        )
    ],
    
)

# 3. zoom the map to the data (Wales)
fig.update_geos(
    projection_type="mercator",
    visible=False,
    resolution=50,
    lonaxis=dict(range=[-6.0, -2.5]),
    lataxis=dict(range=[51.2, 53.6]),

    showland=True,
    landcolor="rgb(220, 220, 220)",

    showocean=True,
    oceancolor="rgb(200, 215, 230)",

    showcoastlines=False,
    coastlinecolor="rgb(110, 110, 110)",
    coastlinewidth=0.6,

    showcountries=False,
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