import pandas as pd
from surprise import Dataset,Reader,SVD
from data_preprocessing import final_df
import joblib

rating_data=final_df[["customer_id","product_id","quantity"]]

reader=Reader(rating_scale=(rating_data["quantity"].min(),
                            rating_data["quantity"].max()))

data=Dataset.load_from_df(rating_data,reader)

trainset=data.build_full_trainset()

model=SVD()

model.fit(trainset)
print("Model trained successfully.")
print(final_df.columns)

prediction=model.predict(uid=1,iid=5)
print("Predicted Rating:",prediction.est)

all_products = final_df["product_id"].unique()

predictions = []

customer_id = 1
purchased_products = final_df[
    final_df["customer_id"] == customer_id
]["product_id"].unique()

print("Purchased Products:", purchased_products)

for product_id in all_products:

    if product_id in purchased_products:
        continue

    prediction = model.predict(uid=customer_id, iid=product_id)

    predictions.append({
        "product_id": product_id,
        "predicted_rating": prediction.est
    })

prediction_df = pd.DataFrame(predictions)

print(prediction_df)

prediction_df=prediction_df.sort_values(
    by="predicted_rating",ascending=False
)
print("prediction_df")
product_info = final_df[["product_id", "product_name", "price"]].drop_duplicates()

recommendations = pd.merge(
    prediction_df,
    product_info,
    on="product_id"
)

recommendations["predicted_rating"] = recommendations["predicted_rating"].round(2)
recommendations = recommendations[
    ["product_name", "price", "predicted_rating"]
]
top_5 = recommendations.head(5)

print("\nTop 5 Recommended Products")
print(top_5)

joblib.dump(model,"svd_model.pkl")
print("Model Saved Successfully")