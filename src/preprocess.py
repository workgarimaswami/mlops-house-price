import pandas as pd
import numpy as np
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_latest_data():
    # look the most recent raw data
    raw_path = "data/raw/latest.csv"

    if not os.path.exists(raw_path):
        logger.error(f"Raw data not found at {raw_path}")
        logger.info("Running data ingestion first...")
        from ingest import download_data
        download_data()

    logger.info(f"Loading data from {raw_path}")
    df = pd.read_csv(raw_path)
    logger.info(f"Loaded data shape : {df.shape}")


    return df

def preprocess_data(df):
    # clean and prepare the data for modelling
    logger.info("Cleaning and preprocessing data...")

    # create a copy
    data=df.copy()

    # 1.handle missing values ( if any)
    if data.isnull().sum().sum()>0:
        logger.info("Filling missing values...")

        # fill numerical columns if missing value with with median

        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].isnull().sum()>0:
                data[col].fillna(data[col].median(), inplace=True)

    # 2. Seperate features and target
    X=data.drop('PRICE', axis=1)
    y=data['PRICE']

    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")

    # 3. Split into train_test_split
    logger.info("Splitting data (80% train, 20% test)...")
    X_train, X_test,y_train,y_test = train_test_split(
        X,y, test_size=0.2, random_state=42, shuffle = True
    )

    # 4.Scale the features
    logger.info("Scaling features...")
    scaler = StandardScaler()

    # fit on training data, tranform both
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # conver back to Dataframes
    X_train = pd.DataFrame(X_train_scaled, columns = X.columns, index=X_train.index)
    X_test = pd.DataFrame(X_test_scaled, columns=X.columns, index=X_test.index)

    # 5. save the scaler for future use
    os.makedirs("models", exist_ok=True)
    scaler_path="models/scaler.pkl"
    joblib.dump(scaler,scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")

    # 6.Save processed data
    save_processed_data(X_train,X_test,y_train,y_test)

    return X_train,X_test,y_train,y_test, scaler

def save_processed_data(X_train,X_test,y_train,y_test):
    """save processed data to disk"""

    logger.info("Saving processed data....")

    processed_path="data/processed"
    os.makedirs(processed_path,exist_ok=True)

    # save as CSV
    X_train.to_csv(f"{processed_path}/X_train.csv", index=False)
    X_test.to_csv(f"{processed_path}/X_test.csv", index=False)
    y_train.to_csv(f"{processed_path}/y_train", index=False)
    y_test.to_csv(f"{processed_path}/y_test", index=False)

    logger.info(f"data saved to {processed_path}/")
    logger.info(f"training samples: {len(X_train)}")
    logger.info(f"test samples : {len(X_test)}")


def main():
    """main preprocessing function"""
    print("=" * 50)
    print("STARTING DATA PREPROCESSING")
    print("="*50)

    # load_data
    df=load_latest_data()

    # preprocess
    X_train, X_test,y_train,y_test,scaler =  preprocess_data(df)

    print("\n" + "=" * 50)
    print("PREPROCESSING COMPLETE!")
    print("=" * 50)
    print(f"Training set : {X_train.shape}")
    print(f"Test set : {X_test.shape}")

    return X_train,X_test,y_train,y_test

if __name__ == "__main__":
    main()