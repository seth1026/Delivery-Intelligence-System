import pandas as pd

df = pd.read_csv("data/Zomato Dataset.csv")
df.columns = df.columns.str.strip()

# Clean minimal (same logic)
df['Time_taken (min)'] = pd.to_numeric(df['Time_taken (min)'], errors='coerce')
df = df.dropna(subset=['Time_taken (min)'])

# -----------------------------
# 1. Traffic Impact
# -----------------------------
traffic_avg = df.groupby('Road_traffic_density')['Time_taken (min)'].mean()

print("\n🚦 Traffic Impact:")
print(traffic_avg)

low = traffic_avg.get('Low', 0)
high = traffic_avg.get('High', 0)

if low > 0:
    increase = ((high - low) / low) * 100
    print(f"\n👉 High traffic increases delivery time by ~{round(increase, 2)}%")


# -----------------------------
# 2. Multiple Deliveries Impact
# -----------------------------
multi_avg = df.groupby('multiple_deliveries')['Time_taken (min)'].mean()

print("\n📦 Multiple Deliveries Impact:")
print(multi_avg)

if 0 in multi_avg and 2 in multi_avg:
    increase = ((multi_avg[2] - multi_avg[0]) / multi_avg[0]) * 100
    print(f"\n👉 2 deliveries increase time by ~{round(increase, 2)}%")


# -----------------------------
# 3. Weather Impact
# -----------------------------
weather_avg = df.groupby('Weather_conditions')['Time_taken (min)'].mean()

print("\n🌦 Weather Impact:")
print(weather_avg.sort_values(ascending=False).head())


# -----------------------------
# 4. Distance Insight (approx)
# -----------------------------
df['distance_bucket'] = pd.cut(df['Time_taken (min)'],
                              bins=[0, 20, 30, 60],
                              labels=['Short', 'Medium', 'Long'])

print("\n📏 Delivery Time Distribution:")
print(df['distance_bucket'].value_counts())