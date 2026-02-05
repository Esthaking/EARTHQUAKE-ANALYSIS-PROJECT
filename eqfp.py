import pandas as pd
import streamlit as st
import sqlalchemy 
from sqlalchemy import create_engine 

engine = create_engine("mysql+pymysql://root:201721@127.0.0.1/seismic_pfl")

def run_query(query):
    return pd.read_sql(query, con=engine)

queries = {
    "Top 10 Strongest Earthquakes": {
        "sql": """
            SELECT mag, depth_km, year, country
            FROM eqmodify_fifth
            ORDER BY mag DESC
            LIMIT 10;
        """,
        "type": "table"
    },

    "Top 10 Deepest Earthquakes": {
        "sql": """
            SELECT depth_km, mag, year, country
            FROM eqmodify_fifth
            ORDER BY depth_km DESC
            LIMIT 10;
        """,
        "type": "table"
    },

    "Shallow & Strong Earthquakes": {
        "sql": """
            SELECT country, mag, depth_km, strenth_category, year
            FROM eqmodify_fifth
            WHERE depth_km < 50 AND mag > 7.5;
        """,
        "type": "table"
    },

    "Average Depth per Country": {
        "sql": """
            SELECT country, AVG(depth_km) AS avg_depth
            FROM eqmodify_fifth
            GROUP BY country
            ORDER BY avg_depth DESC;
        """,
        "type": "bar",
        "index": "country"
    },

    "Average Magnitude by Mag Type": {
        "sql": """
            SELECT magType, AVG(mag) AS avg_mag
            FROM eqmodify_fifth
            GROUP BY magType
            ORDER BY avg_mag DESC;
        """,
        "type": "table"
    },

    "Year with Most Earthquakes": {
        "sql": """
            SELECT year, COUNT(*) AS total
            FROM eqmodify_fifth
            GROUP BY year
            ORDER BY total DESC;
        """,
        "type": "bar",
        "index": "year"
    },

    "Monthly Earthquake Count": {
        "sql": """
            SELECT month, COUNT(*) AS total
            FROM eqmodify_fifth
            GROUP BY month
            ORDER BY total DESC;
        """,
        "type": "table"
    },

    "Earthquakes by Day of Week": {
        "sql": """
            SELECT day_of_week, COUNT(*) AS total
            FROM eqmodify_fifth
            GROUP BY day_of_week
            ORDER BY total DESC;
        """,
        "type": "table"
    },

    "Most Active Reporting Networks": {
        "sql": """
            SELECT net, COUNT(*) AS total
            FROM eqmodify_fifth
            GROUP BY net
            ORDER BY total DESC
            LIMIT 10;
        """,
        "type": "table"
    },

    "Tsunamis per Year": {
        "sql": """
            SELECT year, COUNT(*) AS total
            FROM eqmodify_fifth
            WHERE tsunami = 1
            GROUP BY year;
        """,
        "type": "bar",
        "index": "year"
    }
}


st.title("🌍 Global Seismic Trends Dashboard")

selected_analysis = st.selectbox(
    "Select an analysis",
    list(queries.keys())
)


query_info = queries[selected_analysis]
df_result = run_query(query_info["sql"])

st.subheader(selected_analysis)

if query_info["type"] == "table":
    st.dataframe(df_result)

elif query_info["type"] == "bar":
    st.bar_chart(df_result.set_index(query_info["index"]))
