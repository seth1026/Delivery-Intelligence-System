import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def preprocess_data(df):

    df.columns = df.columns.str.strip()

    # Missing values
    df['Delivery_person_Age'] = df['Delivery_person_Age'].fillna(df['Delivery_person_Age'].median())
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].fillna(df['Delivery_person_Ratings'].median())
    df['multiple_deliveries'] = df['multiple_deliveries'].fillna(df['multiple_deliveries'].median())

    df['Weather_conditions'] = df['Weather_conditions'].fillna(df['Weather_conditions'].mode()[0])
    df['Road_traffic_density'] = df['Road_traffic_density'].fillna(df['Road_traffic_density'].mode()[0])
    df['Festival'] = df['Festival'].fillna(df['Festival'].mode()[0])
    df['City'] = df['City'].fillna(df['City'].mode()[0])

    # Clean invalid
    df = df[df['Delivery_person_Ratings'] <= 5]
    df = df[(df['Delivery_person_Age'] >= 18) & (df['Delivery_person_Age'] <= 60)]

    # Distance
    df['distance_km'] = haversine(
        df['Restaurant_latitude'],
        df['Restaurant_longitude'],
        df['Delivery_location_latitude'],
        df['Delivery_location_longitude']
    )

    # Time features
    df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'], format="%H:%M", errors='coerce')
    df['Time_Order_picked'] = pd.to_datetime(df['Time_Order_picked'], format="%H:%M", errors='coerce')

    df['order_hour'] = df['Time_Orderd'].dt.hour
    df['prep_time'] = (df['Time_Order_picked'] - df['Time_Orderd']).dt.total_seconds() / 60

    df['order_hour'] = df['order_hour'].fillna(df['order_hour'].median())
    df['prep_time'] = df['prep_time'].fillna(df['prep_time'].median())

    # Drop unused
    df = df.drop(['ID', 'Delivery_person_ID', 'Order_Date', 'Time_Orderd', 'Time_Order_picked'], axis=1)

    return df