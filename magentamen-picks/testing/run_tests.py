#!/usr/bin/env python3
"""
Test Runner for Magentamen Picks
Runs all test scripts from the testing directory
"""

import sys
import os
import subprocess

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test(test_name, test_file):
    """Run a specific test and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("Test completed successfully")
            print(result.stdout)
            return True
        else:
            print("Test failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error running test: {e}")
        return False

def main():
    """Run all tests"""
    print("Magentamen Picks Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database Test", "test_database.py"),
        ("Backend Test", "test_backend.py"),
        ("Week Simulation", "simulate_weeks.py")
    ]
    
    results = []
    
    for test_name, test_file in tests:
        success = run_test(test_name, test_file)
        results.append((test_name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}")
    
    passed = 0
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
