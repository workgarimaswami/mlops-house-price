"""
Test the API endpoints
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🧪 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n🧪 Testing model info endpoint...")
    try:
        response = requests.get(f"{API_URL}/model-info")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Model Type: {data.get('model_type')}")
        print(f"   R² Score: {data.get('performance', {}).get('r2_score')}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n🧪 Testing single prediction endpoint...")
    
    # Test data (based on California housing features)
    test_house = {
        "MedInc": 8.3252,
        "HouseAge": 41.0,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322.0,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=test_house)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Prediction successful!")
            print(f"   Predicted Price: ${data['prediction_in_dollars']:,.2f}")
            if 'confidence' in data:
                print(f"   Confidence: {data['confidence']}")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n🧪 Testing batch prediction endpoint...")
    
    # Multiple test houses
    batch_data = {
        "houses": [
            {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.9841,
                "AveBedrms": 1.0238,
                "Population": 322.0,
                "AveOccup": 2.5556,
                "Latitude": 37.88,
                "Longitude": -122.23
            },
            {
                "MedInc": 5.0,
                "HouseAge": 20.0,
                "AveRooms": 4.0,
                "AveBedrms": 1.0,
                "Population": 100.0,
                "AveOccup": 2.0,
                "Latitude": 34.05,
                "Longitude": -118.25
            }
        ]
    }
    
    try:
        response = requests.post(f"{API_URL}/predict-batch", json=batch_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Batch prediction successful!")
            print(f"   Total houses: {data['total_houses']}")
            print(f"   Predictions: {data['predictions_in_dollars']}")
            print(f"   Average price: ${data['average_price']:,.2f}")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 STARTING API TESTS")
    print("=" * 60)
    
    # Wait for API to start
    print("⏳ Waiting for API to be ready...")
    time.sleep(2)
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All tests passed! API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the API logs.")

if __name__ == "__main__":
    main()