import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from preswald import (
    plotly,
    selectbox,
    separator,
    slider,
    text,
    table,
    text_input,
    connect,
    get_df,
)

text("# 🎮 Video Game Sales Analysis")

# Load dataset
connect()
df = get_df("vgsales_csv")  # Ensure dataset is loaded

separator()

text("# Top 10 Best-Selling Games Globally")

# Get the top 10 best-selling games
top_10_games = df.nlargest(10, "Global_Sales")

fig_top_games = px.bar(
    top_10_games.sort_values("Global_Sales", ascending=True),
    x="Global_Sales",
    y="Name",
    orientation="h",
    title="Top 10 Best-Selling Games",
    labels={"Global_Sales": "Global Sales (millions)", "Name": "Game"},
    color="Global_Sales",
    color_continuous_scale="Sunset", 
)

plotly(fig_top_games)


separator()


text("# Annual Global Video Game Sales")

# Remove invalid years
df = df[pd.to_numeric(df["Year"], errors="coerce").notna()]
df["Year"] = df["Year"].astype(int)  # Convert to integer

# Aggregate yearly global sales
sales_per_year = df.groupby("Year")["Global_Sales"].sum()

fig_sales_trend = px.line(
    x=sales_per_year.index,
    y=sales_per_year.values,
    markers=True,
    title="Global Video Game Sales Over the Years",
    labels={"x": "Year", "y": "Total Sales (millions)"}
)

plotly(fig_sales_trend)


separator()


text("# Video Game Platform Market Share")

# Convert 'Year' column to integer
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

# Get valid unique years sorted in ascending order
unique_years = sorted(df["Year"].dropna().unique().tolist())

selected_year = slider(
    "Select Year",
    min_val=min(unique_years),
    max_val=max(unique_years),
    default=min(unique_years)
)

filtered_df = df[df["Year"] == selected_year]

platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().reset_index()

# Remove platforms with zero sales
platform_sales = platform_sales[platform_sales["Global_Sales"] > 0]

fig_platform_pie = px.pie(
    platform_sales,
    names="Platform",
    values="Global_Sales",
    title=f"Platform Sales Distribution in {selected_year}",
    hole=0.4,  # Make it a donut chart
    color_discrete_sequence=px.colors.qualitative.Set3  # Fix color sequence
)

plotly(fig_platform_pie)


separator()


text("# Genre Sales Trends Across Years")

# Text input for selecting a year
year_selected = text_input(
    "Enter Year (1980-2020)", 
    placeholder="e.g., 2003"
)

# Convert to integer if valid, otherwise set a default
try:
    year_selected = int(year_selected)
    if year_selected not in unique_years:
        year_selected = 2003  # Default to 2003 if invalid
except ValueError:
    year_selected = 2003  # Default to 2003 if input is empty

filtered_df = df[df["Year"] == year_selected]

genre_sales = filtered_df.groupby("Genre")["Global_Sales"].sum().reset_index()

genre_sales = genre_sales[genre_sales["Global_Sales"] > 0]

fig_genre_bar = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    title=f"Genre Sales Distribution in {year_selected}",
    labels={"Global_Sales": "Sales (millions)", "Genre": "Game Genre"},
    color="Genre",
    text_auto=True,  
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_genre_bar.update_layout(
    xaxis_tickangle=-45,  # Rotate labels for readability
    barmode="stack"  # Stacked bar format
)

plotly(fig_genre_bar)


separator()


text("# Regional Video Game Sales Explorer")

# Region selection filter
selected_region = selectbox(
    "Select a Region",
    options=["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"],
    default="NA_Sales"
)

# Ensure selected region column is numeric
df[selected_region] = pd.to_numeric(df[selected_region], errors="coerce")

filtered_df = df[df[selected_region] > 0]

filtered_df = filtered_df.sort_values(by=selected_region, ascending=False).head(50)

fig_region_sales = px.bar(
    filtered_df,
    x="Name",
    y=selected_region,
    title=f"Top 50 Best-Selling Games in {selected_region.replace('_', ' ')}",
    labels={selected_region: "Sales (millions)", "Name": "Game"},
    color="Name",
    color_discrete_sequence=px.colors.qualitative.Set3,
    height=500
)

fig_region_sales.update_layout(xaxis_tickangle=-45)

plotly(fig_region_sales)


separator()


text("# Find Top Games by Genre or Platform")

category_type = selectbox(
    "Select Category Type",
    options=["Genre", "Platform"],
    default="Genre"
)

category_options = df[category_type].unique().tolist()

selected_category = selectbox(
    f"Select a {category_type}",
    options=category_options,
    default=category_options[0] 
)

filtered_df = df[df[category_type] == selected_category]


top_games = filtered_df.nlargest(10, "Global_Sales")


fig_category_games = px.bar(
    top_games,
    x="Global_Sales",
    y="Name",
    orientation="h",
    title=f"Top Games in {selected_category} ({category_type})",
    labels={"Global_Sales": "Global Sales (millions)", "Name": "Game"},
    color="Global_Sales",
    color_continuous_scale="Sunset"  # Light theme for consistency
)

plotly(fig_category_games)