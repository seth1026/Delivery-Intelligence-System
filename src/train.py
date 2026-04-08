import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from src.preprocess import preprocess_data

def train_model(df):

    df = preprocess_data(df)

    df = pd.get_dummies(df, columns=[
        'Weather_conditions',
        'Road_traffic_density',
        'Type_of_order',
        'Type_of_vehicle',
        'Festival',
        'City'
    ])

    X = df.drop(['Time_taken (min)', 'Delivery_person_Ratings', 'Delivery_person_Age'], axis=1)
    y = df['Time_taken (min)']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    feature_columns = X.columns

    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)

    return model, feature_columns, importance_df