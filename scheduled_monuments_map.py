# Import libraries 
import pandas as pd
import plotly.express as px

## 1. load the data
df = pd.read_csv("scheduled_monuments_wales_centroids_cleaned.csv")
# pd = pandas (nickname given at library import)
# df = dataframe
# pd.read_csv(...) tells pandas to open a CSV file and read its contents.
# df = ... stores the results in a pandsa DataFrame called df

## Step 1b: Prepare the Period field for animation/sorting

# Explicitly define the chronological order of periods
# This list will be used to force correct time ordering (not alphabetical)
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

# Remove records where the Period value is "Unknown" (So they do not appear in the map animation)
# This filters the dataframe to keep only rows with a known period
df = df[df["Period"] != "Unknown"]
# Create a new version of df that only keeps rows where the Period column is not equal to 'Unknown'
# [df["Period"] = Look at period column in the table.
# != "Unknown"
#   → check each row and ask: is this value NOT “Unknown”?
#   → this produces a True / False result for every row
# df[ ... ]
#   → keep only the rows where the result is True
# df =
#   → overwrite the original dataframe with this filtered version

# Convert the Period column into an ordered categorical type
# This tells pandas (and Plotly) that:
# - Period values come from a fixed list (period_order)
# - The order of that list is meaningful (chronological)
# Without this, periods would be sorted alphabetically
df["Period"] = pd.Categorical(
    df["Period"],
    categories=period_order,
    ordered=True
)

## Step 2. Create the map figure
fig = px.scatter_geo(
    df,                             # The DataFrame (table) that contains all the data
    lon="lon",                      # Column in df that stores longitude values
    lat="lat",                      # Column in df that stores latitude values
    hover_name="Name",              # Column used as the main title in the hover popup
    hover_data=["SAMNumber", "SiteType", "Period"],  
                                    # Extra columns to show when hovering over a point
    animation_frame="Period",       # Creates one trace per animation frame per Period value
    category_orders={"Period": period_order},  
                                    # Forces the animation to follow a specific order
)
# px.scatter_geo(...) builds a Plotly "geo" map using Plotly’s default basemap
# fig is the resulting figure object (the map), stored in memory
# At this stage:
# - the data has been turned into a visual
# - nothing is displayed or saved yet
# - styling and layout tweaks happen in later steps

## Step 3: Configure the geographic basemap / projection / extent
# Update the geographic system of the figure.
# This is specfic to scatter_geo
# it controls map projection, what part of world is visible, land / ocean colouring, coastline and country borders.
# It does not affect marker symbology, hover content, animation frames these are handled by update_traces
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

# Step 4: marker styling and hover behaviour
# Marker styling and hover box content
# trace = one set of plotted figures inside the fig (whole map).
# Apply these settings to every trace in the figure.
fig.update_traces(
    marker=dict(                    # marker symbology
        size=6,                     # Size of each point on the map
        opacity=0.85,               # Slight transparency so overlapping points are visible
        line=dict(
            width=0.5,              # Thickness of the marker outline
            color="white"           # Colour of the marker outline
        )
    ),

    # Custom hover text layout (overrides Plotly's default hover formatting)
    hovertemplate=(
        "<b>%{hovertext}</b><br>"   # Bold title from hover_name (e.g. site name)
        "SAMNumber: %{customdata[0]}<br>"  # First item from hover_data list
        "SiteType: %{customdata[1]}<br>"   # Second item from hover_data list
        "Period: %{customdata[2]}"          # Third item from hover_data list
        "<extra></extra>"           # Removes the default trace name from the hover box
    )
)
# update_traces(...) applies these settings to all markers in the figure
# hovertext comes from hover_name="Name" in px.scatter_geo(...)
# customdata[] comes from the order of items in hover_data=[...]

# Step 5: Page layout
fig.update_layout(
    # Page/layout sizing
    width=1000,
    height=700,
    margin=dict(l=20, r=20, t=70, b=200),

    # Title
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

    # Footnote / attribution
    annotations=[
        dict(
            text=(
                "Designated Historic Asset GIS Data, The Welsh Historic Environment Service (Cadw), "
                "DATE [enter the date you received the data], licensed under the Open Government Licence v3.0.<br>"
                "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
            ),
            x=0.5,
            y=-0.4,
            xref="paper",
            yref="paper",
            xanchor="center",
            yanchor="top",
            showarrow=False,
            font=dict(size=10, color="#555"),
            align="center",
        )
    ],

    # Play / pause controls for the animation
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
                            "frame": {"duration": 800, "redraw": True},  # how long each period stays on screen
                            "transition": {"duration": 500, "easing": "cubic-in-out"},  # smooth fade/move between periods
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
    ],
)

## Step 6: (For develpment) show the map
fig.show()
# opens a temporary, auto-generated preview of the figure.

## step 7: Save to HTML (For Deployment)
fig.write_html("index.html")
# Exports the interactive Plotly map as a standalone HTML file

# Display unique period values
# print(df["Period"].unique())

# print(df["SiteType"].unique())

