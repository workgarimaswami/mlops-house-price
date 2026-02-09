"""
Complete end-to-end MLOps pipeline
"""
import logging
import time
import sys
import os

# Fix Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def run_full_pipeline():
    """
    Run the complete MLOps pipeline:
    1. Data Ingestion
    2. Data Preprocessing
    3. Model Training
    4. Save everything
    """
    start_time = time.time()
    
    print("=" * 60)
    print("🚀 STARTING COMPLETE MLOPS PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Data Ingestion
        logger.info("\n1️⃣  STEP 1: DATA INGESTION")
        
        # Import and run data ingestion
        from ingest import download_data, validate_data
        df = download_data()
        validate_data(df)
        
        # Step 2: Data Preprocessing
        logger.info("\n2️⃣  STEP 2: DATA PREPROCESSING")
        from preprocess import preprocess_data
        X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
        
        # Step 3: Model Training
        logger.info("\n3️⃣  STEP 3: MODEL TRAINING")
        from train import train_model, evaluate_model, save_model, plot_predictions
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)
        
        # Make predictions for plotting
        y_pred = model.predict(X_test)
        plot_predictions(y_test, y_pred)
        
        # Save everything
        model_path, metrics_path = save_model(model, metrics)
        
        # Calculate total time
        total_time = time.time() - start_time
        
        # Final summary
        print("\n" + "=" * 60)
        print("✅ PIPELINE EXECUTION COMPLETE!")
        print("=" * 60)
        print(f"⏱️  Total execution time: {total_time:.2f} seconds")
        print(f"📁 Model saved: {model_path}")
        print(f"📊 Metrics saved: {metrics_path}")
        
        # Display metrics
        if metrics:
            print(f"🎯 Final R² Score: {metrics.get('r2', 'N/A'):.4f}")
            
            # Color code R² score
            r2 = metrics.get('r2', 0)
            if r2 > 0.8:
                r2_display = f"🎉 EXCELLENT: {r2:.4f}"
            elif r2 > 0.6:
                r2_display = f"👍 GOOD: {r2:.4f}"
            elif r2 > 0.4:
                r2_display = f"⚠️  OK: {r2:.4f}"
            else:
                r2_display = f"❌ POOR: {r2:.4f}"
            
            print(f"📈 Model Performance: {r2_display}")
            print(f"📉 RMSE: {metrics.get('rmse', 'N/A'):.4f}")
            print(f"📈 MAE: {metrics.get('mae', 'N/A'):.4f}")
        
        print("\n📋 Next steps:")
        print("   1. Start API: python src/api.py")
        print("   2. Test API: python test_api.py")
        print("   3. View docs: http://localhost:8000/docs")
        print("=" * 60)
        
        return {
            'success': True,
            'model_path': model_path,
            'metrics': metrics,
            'execution_time': total_time
        }
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'success': False,
            'error': str(e)
        }

def run_simple_pipeline():
    """
    Simple pipeline without detailed logging
    """
    print("Running simplified pipeline...")
    
    try:
        # Run individual scripts
        print("1. Ingesting data...")
        os.system("python src/ingest.py")
        
        print("\n2. Preprocessing data...")
        os.system("python src/preprocess.py")
        
        print("\n3. Training model...")
        os.system("python src/train.py")
        
        print("\n✅ Pipeline complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Choose pipeline mode:")
    print("1. Full pipeline (recommended)")
    print("2. Simple pipeline (if full has issues)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        result = run_simple_pipeline()
    else:
        result = run_full_pipeline()
    
    if not result.get('success', False):
        print("\n❌ Pipeline failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        exit(1)