"""Test if server is working"""
import requests
import time

print("Testing detector at http://localhost:5000")

try:
    # Test 1: Homepage
    r = requests.get('http://localhost:5000/', timeout=2)
    print(f"✓ Homepage: {r.status_code}")
    
    # Test 2: Generate traffic
    print("\nGenerating 20 requests...")
    for i in range(20):
        r = requests.get('http://localhost:5000/test', timeout=1)
        print(f"  Request {i+1}: {r.status_code}")
        time.sleep(0.2)
    
    print("\n✓ Test completed!")
    print("Check browser: http://localhost:5000")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure:")
    print("1. Detector is running (python app.py)")
    print("2. Port 5000 is not blocked")
