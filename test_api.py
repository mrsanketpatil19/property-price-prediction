#!/usr/bin/env python3
"""
Test script for the House Price Prediction FastAPI application
"""

import requests
import json

def test_api_predictions():
    """Test the API with different property configurations"""
    
    base_url = "http://localhost:8000/api/predict"
    
    # Test cases with different property configurations
    test_cases = [
        {
            "name": "Average Family Home",
            "params": {
                "building_class": 60,  # 2-STORY 1946 & NEWER
                "lot_size": 8500,
                "overall_material": 7,  # Good
                "house_condition": 5,   # Average
                "house_life": 15,
                "first_floor_area": 1200,
                "grade_living_area": 1500,
                "garage_area": 400,
                "neighborhood": "NAmes",  # North Ames
                "house_type": "1Fam",    # Single Family
                "foundation_type": "PConc"  # Poured Concrete
            }
        },
        {
            "name": "Luxury Home",
            "params": {
                "building_class": 80,  # SPLIT OR MULTI-LEVEL
                "lot_size": 15000,
                "overall_material": 9,  # Very Good
                "house_condition": 8,   # Very Good
                "house_life": 5,
                "first_floor_area": 2000,
                "grade_living_area": 2500,
                "garage_area": 600,
                "neighborhood": "NoRidge",  # Northridge
                "house_type": "1Fam",
                "foundation_type": "PConc"
            }
        },
        {
            "name": "Starter Home",
            "params": {
                "building_class": 20,  # 1-STORY 1946 & NEWER
                "lot_size": 5000,
                "overall_material": 5,  # Average
                "house_condition": 4,   # Below Average
                "house_life": 25,
                "first_floor_area": 800,
                "grade_living_area": 1000,
                "garage_area": 200,
                "neighborhood": "Edwards",  # Edwards
                "house_type": "1Fam",
                "foundation_type": "CBlock"  # Cinder Block
            }
        }
    ]
    
    print("🏠 House Price Prediction API Test")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 30)
        
        try:
            response = requests.get(base_url, params=test_case['params'])
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Prediction: {result['predicted_price']}")
                print(f"📊 Raw Value: ${result['predicted_price_raw']:,.2f}")
                
                # Show key features
                features = result['input_features']
                print(f"🏗️  Building Class: {features['Building_Class']}")
                print(f"📏 Lot Size: {features['Lot_Size']:,} sq ft")
                print(f"⭐ Material Quality: {features['Overall_Material']}/10")
                print(f"🏘️  Neighborhood: {features['Neighborhood']}")
                print(f"🏠 House Type: {features['House_Type']}")
                print(f"🏗️  Foundation: {features['Foundation_Type']}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to the API server")
            print("Make sure the FastAPI application is running on http://localhost:8000")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\nTo use the web interface, visit: http://localhost:8000")
    print("For API documentation, visit: http://localhost:8000/docs")

if __name__ == "__main__":
    test_api_predictions() 