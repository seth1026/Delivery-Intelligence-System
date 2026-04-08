import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.train import train_model
from src.predict import predict

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Delivery Intelligence Dashboard", layout="wide")

st.title("🚚 Delivery Intelligence Dashboard")
st.markdown("Predict delivery time and analyze key operational factors")


# =========================
# LOAD DATA + MODEL
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data/Zomato Dataset.csv")


@st.cache_resource
def load_model(df):
    model, feature_columns, importance_df = train_model(df)
    return model, feature_columns, importance_df


df = load_data()
model, feature_columns, importance_df = load_model(df)


# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("📥 Input Parameters")

distance = st.sidebar.slider("Distance (km)", 1.0, 20.0, 5.0)
prep_time = st.sidebar.slider("Preparation Time (min)", 5, 40, 15)
order_hour = st.sidebar.slider("Order Hour", 0, 23, 20)

multiple_deliveries = st.sidebar.selectbox("Multiple Deliveries", [0, 1, 2, 3])
vehicle_condition = st.sidebar.selectbox("Vehicle Condition", [0, 1, 2, 3])

weather = st.sidebar.selectbox("Weather", ["Sunny", "Fog", "Stormy", "Sandstorms", "Cloudy"])
traffic = st.sidebar.selectbox("Traffic", ["Low", "Medium", "High", "Jam"])
order_type = st.sidebar.selectbox("Order Type", ["Meal", "Snack", "Drinks"])
vehicle_type = st.sidebar.selectbox("Vehicle", ["motorcycle", "scooter"])
festival = st.sidebar.selectbox("Festival", ["Yes", "No"])
city = st.sidebar.selectbox("City", ["Metropolitian", "Urban", "Semi-Urban"])


# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns([1, 1])


# =========================
# PREDICTION SECTION
# =========================
with col1:
    st.subheader("⏱ Delivery Time Prediction")

    if st.button("🚀 Predict Delivery Time"):

        input_data = {
            'Vehicle_condition': vehicle_condition,
            'multiple_deliveries': multiple_deliveries,
            'distance_km': distance,
            'order_hour': order_hour,
            'prep_time': prep_time,

            'Weather_conditions': weather,
            'Road_traffic_density': traffic,
            'Type_of_order': order_type,
            'Type_of_vehicle': vehicle_type,
            'Festival': festival,
            'City': city
        }

        result = predict(input_data, model, feature_columns)

        st.success(f"Estimated Delivery Time: **{round(result, 2)} minutes**")


# =========================
# FEATURE IMPORTANCE
# =========================
with col2:
    st.subheader("📊 Feature Importance")

    fig, ax = plt.subplots()
    importance_df.head(10).plot(
        kind='barh',
        x='feature',
        y='importance',
        ax=ax
    )
    ax.invert_yaxis()

    st.pyplot(fig)


# =========================
# INSIGHTS SECTION
# =========================
st.markdown("---")
st.subheader("🧠 Key Insights")

st.markdown("""
- 🚗 **Distance** is the strongest driver of delivery time  
- 📦 **Multiple deliveries** significantly increase delays  
- 🚦 **Traffic conditions** have a major operational impact  
- 🌦 **Weather variability** affects delivery efficiency  
""")


# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Built with ❤️ using Machine Learning & Streamlit")