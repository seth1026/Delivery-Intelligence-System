import pandas as pd

def predict(input_dict, model, feature_columns):

    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    return model.predict(input_df)[0]