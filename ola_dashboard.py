import streamlit as st
import pandas as pd
from sqlalchemy import text
from db_connection import get_connection
import time
from datetime import datetime

# ==========================
# Get DB Connection
# ==========================
# Global Engine
engine = get_connection()

# ==========================
# Page Config & CSS
# ==========================
st.set_page_config(page_title="🚖 OLA SQL Analytics", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .analytics-header {
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .query-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2c5364;
    }
    .sql-code {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
    }
    .result-summary {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #b8daff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# Main Header
# ==========================
st.markdown("""
<div class="analytics-header">
    <h1>🚖 OLA Rides SQL Analytics</h1>
    <p>Run interactive SQL queries with one click and analyze booking data</p>
</div>
""", unsafe_allow_html=True)

# ==========================
# Queries
# ==========================
QUERIES = {
    1: {
        "title": "All Successful Bookings",
        "description": "Retrieve all rides where booking status is successful.",
        "sql": "SELECT * FROM ola_rides WHERE Booking_Status = 'Success';"
    },
    2: {
        "title": "Average Ride Distance per Vehicle Type",
        "description": "Calculate the average ride distance for each type of vehicle.",
        "sql": """
            SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS avg_distance
            FROM ola_rides
            WHERE Ride_Distance > 0
            GROUP BY Vehicle_Type
            ORDER BY avg_distance DESC;
        """
    },
    3: {
        "title": "Total Cancelled Rides by Customers",
        "description": "Get total number of rides cancelled by customers.",
        "sql": """
            SELECT COUNT(*) AS total_cancelled_by_customers
            FROM ola_rides
            WHERE Booking_Status = 'Canceled by Customer';
        """
    },
    4: {
        "title": "Top 5 Customers by Number of Rides",
        "description": "Find the top 5 customers who booked the highest number of rides.",
        "sql": """
            SELECT Customer_ID, COUNT(*) AS total_rides
            FROM ola_rides
            GROUP BY Customer_ID
            ORDER BY total_rides DESC
            LIMIT 5;
        """
    },
    5: {
        "title": "Rides Cancelled by Drivers (Personal/Car Issues)",
        "description": "Count rides cancelled by drivers due to personal or car-related issues.",
        "sql": """
            SELECT COUNT(*) AS cancelled_by_driver_personal_car_issue
            FROM ola_rides
            WHERE Booking_Status = 'Canceled by Driver'
              AND Canceled_Rides_by_Driver = 'Personal & Car related issue';
        """
    },
    6: {
        "title": "Max & Min Driver Ratings (Prime Sedan)",
        "description": "Find the maximum and minimum driver ratings for Prime Sedan bookings.",
        "sql": """
            SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating
            FROM ola_rides
            WHERE Vehicle_Type = 'Prime Sedan'
              AND Driver_Ratings IS NOT NULL;
        """
    },
    7: {
        "title": "Rides Paid via UPI",
        "description": "Retrieve all rides where payment was made using UPI.",
        "sql": "SELECT * FROM ola_rides WHERE Payment_Method = 'Upi';"
    },
    8: {
        "title": "Average Customer Rating per Vehicle Type",
        "description": "Calculate the average customer rating grouped by vehicle type.",
        "sql": """
            SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating
            FROM ola_rides
            WHERE Customer_Rating IS NOT NULL
            GROUP BY Vehicle_Type
            ORDER BY avg_customer_rating DESC;
        """
    },
    9: {
        "title": "Total Booking Value of Successful Rides",
        "description": "Get the total revenue generated from successful rides.",
        "sql": """
            SELECT SUM(Booking_Value) AS total_success_booking_value
            FROM ola_rides
            WHERE Booking_Status = 'Success';
        """
    },
    10: {
        "title": "Incomplete Rides with Reason",
        "description": "List all incomplete rides with their reasons.",
        "sql": """
            SELECT Booking_ID, Customer_ID, Vehicle_Type, Incomplete_Rides_Reason
            FROM ola_rides
            WHERE Incomplete_Rides = 'Yes';
        """
    }
}

# ==========================
# Query Runner
# ==========================
def execute_query(query, title):
    try:
        start_time = time.time()
        with engine.connect() as conn:   # ✅ Safe context manager
            result = conn.execute(text(query))
            exec_time = round((time.time() - start_time) * 1000, 2)
            columns = list(result.keys())
            rows = result.fetchall()

            if rows:
                df = pd.DataFrame(rows, columns=columns)
                st.success(f"✅ Query executed in {exec_time} ms")
                return df, exec_time
            else:
                st.warning("📭 No data returned")
                return None, exec_time
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        return None, 0

# ==========================
# Display Queries
# ==========================
for q_num, q_info in QUERIES.items():
    st.markdown('<div class="query-section">', unsafe_allow_html=True)

    st.markdown(f"### Q{q_num}: {q_info['title']}")
    st.markdown(f"**Description:** {q_info['description']}")

    with st.expander(f"📝 View SQL Code - Query {q_num}"):
        st.markdown(f'<div class="sql-code">{q_info["sql"]}</div>', unsafe_allow_html=True)

    if st.button(f"🚀 Run Query {q_num}", key=f"run_{q_num}"):
        with st.spinner("⏳ Executing..."):
            df, exec_time = execute_query(q_info["sql"], q_info["title"])
            if df is not None:
                st.markdown(f"""
                <div class="result-summary">
                    <strong>📊 Results Summary:</strong><br>
                    • Rows returned: {len(df)}<br>
                    • Columns: {len(df.columns)}<br>
                    • Execution time: {exec_time} ms
                </div>
                """, unsafe_allow_html=True)

                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"ola_query_{q_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

# ==========================
# Sidebar Stats
# ==========================
st.sidebar.title("🚖 OLA SQL Analytics")
st.sidebar.metric("Total Queries", len(QUERIES))
st.sidebar.metric("Successful Runs", "Click buttons to execute")

st.markdown("---")
st.markdown(f"*📊 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")