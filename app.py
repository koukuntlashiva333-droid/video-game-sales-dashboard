import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.kpi-card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    color: #222222;
}


.kpi-title {
    font-size: 16px;
    color: #555555 !important;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #111111 !important;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("final_cleaned_video_games.csv")
    return data


df = load_data()


# ---------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------

df["Year_of_Release"] = pd.to_numeric(
    df["Year_of_Release"],
    errors="coerce"
)

df = df.dropna(subset=["Year_of_Release"])

df["Year_of_Release"] = df["Year_of_Release"].astype(int)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown(
    '<div class="dashboard-title">🎮 Video Game Sales Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Exploring the factors behind video game success'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🎯 Dashboard Filters")

# Genre filter
genres = sorted(df["Genre"].dropna().unique())

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    genres,
    default=genres
)

# Platform filter
platforms = sorted(df["Platform"].dropna().unique())

selected_platforms = st.sidebar.multiselect(
    "Select Platform",
    platforms,
    default=platforms
)

# Publisher filter
publishers = sorted(df["Publisher"].dropna().unique())

selected_publishers = st.sidebar.multiselect(
    "Select Publisher",
    publishers,
    default=publishers
)

# Year filter
min_year = int(df["Year_of_Release"].min())
max_year = int(df["Year_of_Release"].max())

selected_years = st.sidebar.slider(
    "Release Year",
    min_year,
    max_year,
    (min_year, max_year)
)


# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered_df = df[
    (df["Genre"].isin(selected_genres)) &
    (df["Platform"].isin(selected_platforms)) &
    (df["Publisher"].isin(selected_publishers)) &
    (df["Year_of_Release"].between(
        selected_years[0],
        selected_years[1]
    ))
]


# ---------------------------------------------------
# CHECK EMPTY DATA
# ---------------------------------------------------

if filtered_df.empty:

    st.warning(
        "No games match the selected filters. "
        "Please change the filters."
    )

    st.stop()


# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_games = len(filtered_df)

total_sales = filtered_df["Global_Sales"].sum()

average_sales = filtered_df["Global_Sales"].mean()

top_genre = (
    filtered_df.groupby("Genre")["Global_Sales"]
    .sum()
    .idxmax()
)


# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🎮 Total Games</div>
            <div class="kpi-value">{total_games:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🌍 Global Sales</div>
            <div class="kpi-value">{total_sales:,.2f} M</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📊 Average Sales</div>
            <div class="kpi-value">{average_sales:.2f} M</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🏆 Top Genre</div>
            <div class="kpi-value">{top_genre}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")


# ---------------------------------------------------
# CHART 1: SALES BY GENRE
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Sales Performance</div>',
    unsafe_allow_html=True
)

genre_sales = (
    filtered_df
    .groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_genre = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    title="Global Sales by Genre",
    labels={
        "Genre": "Genre",
        "Global_Sales": "Global Sales (Millions)"
    },
    text_auto=".2f"
)

fig_genre.update_layout(
    xaxis_title="Game Genre",
    yaxis_title="Global Sales (Millions)",
    hovermode="x unified"
)

st.plotly_chart(
    fig_genre,
    use_container_width=True
)


# ---------------------------------------------------
# CHART 2: SALES OVER TIME
# ---------------------------------------------------

year_sales = (
    filtered_df
    .groupby("Year_of_Release")["Global_Sales"]
    .sum()
    .reset_index()
    .sort_values("Year_of_Release")
)

fig_year = px.line(
    year_sales,
    x="Year_of_Release",
    y="Global_Sales",
    markers=True,
    title="Global Video Game Sales Over Time",
    labels={
        "Year_of_Release": "Release Year",
        "Global_Sales": "Global Sales (Millions)"
    }
)

fig_year.update_layout(
    xaxis_title="Release Year",
    yaxis_title="Global Sales (Millions)"
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# ---------------------------------------------------
# TWO COLUMN SECTION
# ---------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------
# CHART 3: REGIONAL SALES
# ---------------------------------------------------

with col1:

    regional_sales = (
        filtered_df
        .groupby("Genre")[
            ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
        ]
        .sum()
        .reset_index()
    )

    regional_long = regional_sales.melt(
        id_vars="Genre",
        value_vars=[
            "NA_Sales",
            "EU_Sales",
            "JP_Sales",
            "Other_Sales"
        ],
        var_name="Region",
        value_name="Sales"
    )

    region_names = {
        "NA_Sales": "North America",
        "EU_Sales": "Europe",
        "JP_Sales": "Japan",
        "Other_Sales": "Other Regions"
    }

    regional_long["Region"] = (
        regional_long["Region"]
        .replace(region_names)
    )

    fig_region = px.bar(
        regional_long,
        x="Genre",
        y="Sales",
        color="Region",
        barmode="group",
        title="Regional Sales by Genre",
        labels={
            "Genre": "Genre",
            "Sales": "Sales (Millions)",
            "Region": "Region"
        }
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ---------------------------------------------------
# CHART 4: CRITIC SCORE VS SALES
# ---------------------------------------------------

with col2:

    critic_data = filtered_df.dropna(
        subset=["Critic_Score"]
    )

    fig_critic = px.scatter(
        critic_data,
        x="Critic_Score",
        y="Global_Sales",
        color="Genre",
        hover_name="Name",
        hover_data=[
            "Platform",
            "Year_of_Release"
        ],
        title="Critic Score vs Global Sales",
        labels={
            "Critic_Score": "Critic Score",
            "Global_Sales": "Global Sales (Millions)"
        },
        opacity=0.65
    )

    st.plotly_chart(
        fig_critic,
        use_container_width=True
    )


# ---------------------------------------------------
# TOP 10 GAMES
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">🏆 Top 10 Best-Selling Games</div>',
    unsafe_allow_html=True
)

top_games = (
    filtered_df[
        [
            "Name",
            "Platform",
            "Genre",
            "Year_of_Release",
            "Global_Sales"
        ]
    ]
    .sort_values(
        "Global_Sales",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_games,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------
# FILTERED DATA
# ---------------------------------------------------

with st.expander("📋 View Filtered Dataset"):

    st.write(
        f"Showing {len(filtered_df):,} games"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        🎮 Video Game Sales Analysis |
        Fundamentals of Data Science Project
    </div>
    """,
    unsafe_allow_html=True
)