import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

# Create sample data (or use your actual data)
data = {
    'area': [2600, 3000, 3200, 3600, 4000],
    'bedrooms': [3, 4, 4, 3, 5],
    'age': [20, 15, 18, 30, 8],
    'price': [550000, 565000, 610000, 595000, 760000]
}

df = pd.DataFrame(data)

# Prepare features and target
X = df[['area', 'bedrooms', 'age']]
y = df['price']

# Train model
model = LinearRegression()
model.fit(X, y)

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Save model
with open('model/house_price_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved to model/house_price_model.pkl")
print(f"Model coefficients: {model.coef_}")
print(f"Model intercept: {model.intercept_}")