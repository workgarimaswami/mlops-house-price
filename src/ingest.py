"""
Improved data ingestion with REALISTIC patterns
"""
import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def create_realistic_housing_data(n_samples=1000):
    """
    Create synthetic housing data with REAL patterns
    """
    np.random.seed(42)
    
    # REALISTIC PATTERNS:
    # 1. Higher income → Higher price
    # 2. More rooms → Higher price  
    # 3. Newer houses → Higher price
    # 4. Good location (lat/long) → Higher price
    
    # Create base features with patterns
    income = np.random.uniform(2, 15, n_samples)  # Median income
    
    # Price is strongly correlated with income
    base_price = income * 30 + np.random.normal(0, 10, n_samples)
    
    # More rooms increase price
    rooms = np.random.uniform(3, 10, n_samples)
    base_price += rooms * 15
    
    # Newer houses are more expensive
    house_age = np.random.uniform(1, 50, n_samples)
    base_price -= house_age * 0.5  # Older = cheaper
    
    # Good location increases price
    latitude = np.random.uniform(34, 38, n_samples)  # California range
    longitude = np.random.uniform(-122, -118, n_samples)
    
    # SF Bay Area (lat 37-38, long -122 to -121) is expensive
    in_bay_area = (latitude > 37) & (latitude < 38) & (longitude > -122) & (longitude < -121)
    base_price += in_bay_area * 100
    
    # Add some randomness but keep pattern
    final_price = base_price + np.random.normal(0, 20, n_samples)
    
    # Ensure prices are positive
    final_price = np.maximum(final_price, 50)
    
    # Create other features with some correlation
    bedrooms = rooms * 0.7 + np.random.normal(0, 0.3, n_samples)
    population = np.random.uniform(100, 3000, n_samples)
    occupancy = population / (income * 100) + np.random.normal(2, 1, n_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'MedInc': np.round(income, 4),
        'HouseAge': np.round(house_age, 1),
        'AveRooms': np.round(rooms, 4),
        'AveBedrms': np.round(bedrooms, 4),
        'Population': np.round(population, 0),
        'AveOccup': np.round(occupancy, 4),
        'Latitude': np.round(latitude, 2),
        'Longitude': np.round(longitude, 2),
        'PRICE': np.round(final_price, 2)
    })
    
    return df

def download_data():
    """
    Create realistic housing data
    """
    logger.info("🚀 Creating REALISTIC housing data with patterns...")
    
    # Create data with patterns
    df = create_realistic_housing_data(n_samples=1000)
    
    logger.info(f"✅ Data created! Shape: {df.shape}")
    
    # Calculate correlations to show patterns
    correlations = df.corr()['PRICE'].sort_values(ascending=False)
    print("\n📊 Feature correlations with PRICE:")
    for feature, corr in correlations.items():
        if feature != 'PRICE':
            print(f"   {feature}: {corr:.3f}")
    
    # Save data
    raw_path = os.path.join("data", "raw")
    os.makedirs(raw_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"housing_data_{timestamp}.csv"
    filepath = os.path.join(raw_path, filename)
    
    df.to_csv(filepath, index=False)
    df.to_csv(os.path.join(raw_path, "latest.csv"), index=False)
    
    print(f"\n📊 Sample data (first 3 rows):")
    print(df.head(3).to_string())
    
    print(f"\n📈 Price statistics:")
    print(f"   Min: ${df['PRICE'].min():.2f}k")
    print(f"   Max: ${df['PRICE'].max():.2f}k")
    print(f"   Mean: ${df['PRICE'].mean():.2f}k")
    
    print(f"\n💾 Saved to: {filepath}")
    
    return df

def validate_data(df):
    """
    Validate data
    """
    print("\n🔍 Validating data...")
    
    # Check correlations
    corr_with_price = df.corr()['PRICE'].abs().sort_values(ascending=False)
    
    print("📊 Absolute correlation with PRICE (higher = better pattern):")
    for feature, corr in corr_with_price.items():
        if feature != 'PRICE':
            star = "🌟" if corr > 0.3 else "⭐" if corr > 0.1 else ""
            print(f"   {feature}: {corr:.3f} {star}")
    
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("CREATING REALISTIC HOUSING DATA")
    print("=" * 50)
    
    df = download_data()
    validate_data(df)
    
    print("\n" + "=" * 50)
    print("✅ DATA CREATION COMPLETE!")
    print("=" * 50)
    
    return df

if __name__ == "__main__":
    main()