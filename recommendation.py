import pandas as pd
import joblib
from data_preprocessing import final_df

# Load trained model
model = joblib.load("svd_model.pkl")


def recommend_products(customer_id):

    all_products = final_df["product_id"].unique()

    purchased_products = final_df[
        final_df["customer_id"] == customer_id
    ]["product_id"].unique()

    predictions = []

    for product_id in all_products:

        if product_id in purchased_products:
            continue

        prediction = model.predict(uid=customer_id, iid=product_id)

        predictions.append({
            "product_id": product_id,
            "predicted_rating": prediction.est
        })

    prediction_df = pd.DataFrame(predictions)

    prediction_df = prediction_df.sort_values(
        by="predicted_rating",
        ascending=False
    )

    product_info = final_df[
        ["product_id", "product_name", "price"]
    ].drop_duplicates()

    recommendations = pd.merge(
        prediction_df,
        product_info,
        on="product_id"
    )

    return recommendations.head(5)