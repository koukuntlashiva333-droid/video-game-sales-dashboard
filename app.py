import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================
   MAIN DASHBOARD BACKGROUND
   ========================================= */

.stApp {
    background-color: #f5f7fb;
}


/* =========================================
   DASHBOARD TITLE
   ========================================= */

h1 {
    color: #6C2BD9 !important;
    font-weight: 800 !important;
    text-align: center !important;
    font-size: 42px !important;
}


/* =========================================
   SUBTITLE
   ========================================= */

.dashboard-subtitle {
    text-align: center;
    font-size: 18px;
    color: #666666 !important;
    margin-bottom: 30px;
}


/* =========================================
   KPI CARDS
   ========================================= */

div[data-testid="stMetric"] {
    background-color: white !important;
    padding: 20px !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    text-align: center !important;
    min-height: 120px !important;
}


/* =========================================
   KPI NAMES
   Total Games
   Global Sales
   Average Sales
   Top Genre
   ========================================= */

div[data-testid="stMetricLabel"] {
    color: #6C2BD9 !important;
    font-weight: 700 !important;
}


/* Force the color on everything INSIDE the label */
div[data-testid="stMetricLabel"] * {
    color: #6C2BD9 !important;
}


/* Also target paragraph text */
div[data-testid="stMetricLabel"] p {
    color: #6C2BD9 !important;
    font-weight: 700 !important;
}


/* =========================================
   KPI VALUES
   ========================================= */

div[data-testid="stMetricValue"] {
    color: #111111 !important;
    font-weight: 700 !important;
    font-size: 28px !important;
}


/* Force value text to stay dark */
div[data-testid="stMetricValue"] * {
    color: #111111 !important;
}


/* =========================================
   SECTION TITLES
   ========================================= */

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #222222 !important;
}


/* =========================================
   FILTER INFORMATION
   ========================================= */

.filter-info {
    padding: 12px;
    border-radius: 10px;
    background-color: white !important;
    text-align: center;
    font-weight: 600;
    color: #444444 !important;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv(
        "final_cleaned_video_games.csv"
    )

    return data


df = load_data()


# ============================================================
# DATA PREPARATION
# ============================================================

df["Year_of_Release"] = pd.to_numeric(
    df["Year_of_Release"],
    errors="coerce"
)

df = df.dropna(
    subset=["Year_of_Release"]
)

df["Year_of_Release"] = (
    df["Year_of_Release"].astype(int)
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🎮 Video Game Sales Dashboard"
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Exploring the factors behind video game success'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header(
    "🎯 Dashboard Filters"
)

st.sidebar.write(
    "Filters are optional. "
    "Leave a filter empty to include all values."
)


# ============================================================
# GENRE FILTER
# ============================================================

genres = sorted(
    df["Genre"]
    .dropna()
    .unique()
)

selected_genres = st.sidebar.multiselect(
    "🎮 Genre",
    options=genres,
    default=[],
    placeholder="Select genre(s)"
)


# ============================================================
# PLATFORM FILTER
# ============================================================

platforms = sorted(
    df["Platform"]
    .dropna()
    .unique()
)

selected_platforms = st.sidebar.multiselect(
    "🕹️ Platform",
    options=platforms,
    default=[],
    placeholder="Select platform(s)"
)


# ============================================================
# PUBLISHER FILTER
# ============================================================

publishers = sorted(
    df["Publisher"]
    .dropna()
    .unique()
)

selected_publishers = st.sidebar.multiselect(
    "🏢 Publisher",
    options=publishers,
    default=[],
    placeholder="Select publisher(s)"
)


# ============================================================
# YEAR FILTER
# ============================================================

min_year = int(
    df["Year_of_Release"].min()
)

max_year = int(
    df["Year_of_Release"].max()
)

selected_years = st.sidebar.slider(
    "📅 Release Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# ============================================================
# CLEAR ALL FILTERS
# ============================================================

if st.sidebar.button(
    "🔄 Clear All Filters",
    use_container_width=True
):

    st.rerun()


# ============================================================
# APPLY OPTIONAL FILTERS
# ============================================================

filtered_df = df.copy()


# -----------------------------
# Genre
# -----------------------------

if selected_genres:

    filtered_df = filtered_df[
        filtered_df["Genre"].isin(
            selected_genres
        )
    ]


# -----------------------------
# Platform
# -----------------------------

if selected_platforms:

    filtered_df = filtered_df[
        filtered_df["Platform"].isin(
            selected_platforms
        )
    ]


# -----------------------------
# Publisher
# -----------------------------

if selected_publishers:

    filtered_df = filtered_df[
        filtered_df["Publisher"].isin(
            selected_publishers
        )
    ]


# -----------------------------
# Year
# -----------------------------

filtered_df = filtered_df[
    filtered_df["Year_of_Release"].between(
        selected_years[0],
        selected_years[1]
    )
]


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No games match the selected filters. "
        "Try selecting different filters."
    )

    st.stop()


# ============================================================
# FILTER INFORMATION
# ============================================================

st.markdown(
    f"""
    <div class="filter-info">
        Showing {len(filtered_df):,} games
        out of {len(df):,} total games
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_games = len(
    filtered_df
)

total_sales = (
    filtered_df["Global_Sales"].sum()
)

average_sales = (
    filtered_df["Global_Sales"].mean()
)

top_genre = (
    filtered_df
    .groupby("Genre")["Global_Sales"]
    .sum()
    .idxmax()
)


# ============================================================
# KPI CARDS
# ============================================================

# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.html(f"""
    <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        min-height:100px;
    ">
        <div style="
            color:#6C2BD9;
            font-size:16px;
            font-weight:700;
            margin-bottom:12px;
        ">
            🎮 Total Games
        </div>

        <div style="
            color:#111111;
            font-size:28px;
            font-weight:700;
        ">
            {total_games:,}
        </div>
    </div>
    """)


with col2:
    st.html(f"""
    <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        min-height:100px;
    ">
        <div style="
            color:#6C2BD9;
            font-size:16px;
            font-weight:700;
            margin-bottom:12px;
        ">
            🌍 Global Sales
        </div>

        <div style="
            color:#111111;
            font-size:28px;
            font-weight:700;
        ">
            {total_sales:,.2f} M
        </div>
    </div>
    """)


with col3:
    st.html(f"""
    <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        min-height:100px;
    ">
        <div style="
            color:#6C2BD9;
            font-size:16px;
            font-weight:700;
            margin-bottom:12px;
        ">
            📊 Average Sales
        </div>

        <div style="
            color:#111111;
            font-size:28px;
            font-weight:700;
        ">
            {average_sales:.2f} M
        </div>
    </div>
    """)


with col4:
    st.html(f"""
    <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        min-height:100px;
    ">
        <div style="
            color:#6C2BD9;
            font-size:16px;
            font-weight:700;
            margin-bottom:12px;
        ">
            🏆 Top Genre
        </div>

        <div style="
            color:#111111;
            font-size:28px;
            font-weight:700;
        ">
            {top_genre}
        </div>
    </div>
    """)


st.markdown("---")


# ============================================================
# CHART 1
# GLOBAL SALES BY GENRE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Global Sales by Genre'
    '</div>',
    unsafe_allow_html=True
)


genre_sales = (
    filtered_df
    .groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


fig_genre = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    title="Global Sales by Genre",
    labels={
        "Genre": "Game Genre",
        "Global_Sales":
            "Global Sales (Millions)"
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


# ============================================================
# CHART 2
# SALES OVER TIME
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 Global Sales Over Time'
    '</div>',
    unsafe_allow_html=True
)


year_sales = (
    filtered_df
    .groupby("Year_of_Release")[
        "Global_Sales"
    ]
    .sum()
    .reset_index()
    .sort_values(
        "Year_of_Release"
    )
)


fig_year = px.line(
    year_sales,
    x="Year_of_Release",
    y="Global_Sales",
    markers=True,
    title="Global Video Game Sales Over Time",
    labels={
        "Year_of_Release":
            "Release Year",
        "Global_Sales":
            "Global Sales (Millions)"
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


# ============================================================
# TWO COLUMN SECTION
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# CHART 3
# REGIONAL SALES
# ============================================================

with col1:

    regional_sales = (
        filtered_df
        .groupby("Genre")[
            [
                "NA_Sales",
                "EU_Sales",
                "JP_Sales",
                "Other_Sales"
            ]
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

        "NA_Sales":
            "North America",

        "EU_Sales":
            "Europe",

        "JP_Sales":
            "Japan",

        "Other_Sales":
            "Other Regions"
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
            "Genre":
                "Game Genre",

            "Sales":
                "Sales (Millions)",

            "Region":
                "Region"
        }
    )


    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ============================================================
# CHART 4
# CRITIC SCORE VS GLOBAL SALES
# ============================================================

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
            "Critic_Score":
                "Critic Score",

            "Global_Sales":
                "Global Sales (Millions)"
        },
        opacity=0.65
    )


    st.plotly_chart(
        fig_critic,
        use_container_width=True
    )


# ============================================================
# TOP 10 GAMES
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🏆 Top 10 Best-Selling Games'
    '</div>',
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


# ============================================================
# FILTERED DATASET
# ============================================================

with st.expander(
    "📋 View Filtered Dataset"
):

    st.write(
        f"Showing {len(filtered_df):,} games"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.markdown(
    """
    <div style="
        text-align:center;
        color:#777;
        padding:10px;
    ">

        🎮 Video Game Sales Analysis |
        Fundamentals of Data Science Project

    </div>
    """,
    unsafe_allow_html=True
)
