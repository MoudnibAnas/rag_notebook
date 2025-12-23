#!/usr/bin/env python3
"""
Frontend API Test Script
Tests the optimized Local RAG Debate System frontend endpoints
"""

import requests
import time
import json

def test_frontend():
    base_url = "http://localhost:5000"
    
    print("="*60)
    print("FRONTEND API TEST")
    print("="*60)
    
    # Test 1: Main page
    print("\n1. Testing main page...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code} - {'PASS' if response.status_code == 200 else 'FAIL'}")
        if response.status_code == 200:
            print(f"   Content length: {len(response.text)} characters")
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
    
    # Test 2: Test endpoint
    print("\n2. Testing test endpoint...")
    try:
        response = requests.get(f"{base_url}/test", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
            print("   PASS")
        else:
            print("   ✗ FAIL")
    except Exception as e:
        print(f"   FAIL: {e}")
    
    # Test 3: Documents endpoint
    print("\n3. Testing documents endpoint...")
    try:
        response = requests.get(f"{base_url}/documents", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Documents found: {len(data.get('documents', []))}")
            print(f"   Response: {data}")
            print("   ✓ PASS")
        else:
            print("   ✗ FAIL")
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
    
    # Test 4: Generate endpoint (dry run)
    print("\n4. Testing generate endpoint (dry run)...")
    try:
        test_data = {"topic": "What is the main topic of the documents?"}
        response = requests.post(
            f"{base_url}/generate", 
            json=test_data, 
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success', False)}")
            if data.get('success'):
                print("   ✓ PASS - Generation endpoint working")
            else:
                print(f"   Error: {data.get('error', 'Unknown error')}")
        else:
            print("   ✗ FAIL")
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
    
    print("\n" + "="*60)
    print("FRONTEND TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_frontend()