"""
Test script for validation improvements.
Run this alongside the Flask server to test all validation cases.
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_case(name, data, expected_status):
    """Test a single case and print results."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"Data: {data}")

    try:
        response = requests.post(
            f"{BASE_URL}/update",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code} (expected {expected_status})")
        print(f"Response: {response.json()}")

        if response.status_code == expected_status:
            print("✓ PASS")
        else:
            print("✗ FAIL")
    except Exception as e:
        print(f"✗ ERROR: {e}")

if __name__ == "__main__":
    print("Testing Flask IoT API Validation")
    print("Make sure the server is running on port 5000")

    # Valid case
    test_case(
        "Valid data",
        {"temperature": 23.5, "humidity": 60},
        200
    )

    # Missing JSON body
    print("\n" + "="*60)
    print("TEST: Missing JSON body")
    try:
        response = requests.post(f"{BASE_URL}/update")
        print(f"Status: {response.status_code} (expected 400)")
        print(f"Response: {response.json()}")
        print("✓ PASS" if response.status_code == 400 else "✗ FAIL")
    except Exception as e:
        print(f"✗ ERROR: {e}")

    # Missing temperature field
    test_case(
        "Missing temperature",
        {"humidity": 60},
        400
    )

    # Missing humidity field
    test_case(
        "Missing humidity",
        {"temperature": 23.5},
        400
    )

    # Invalid temperature type
    test_case(
        "Invalid temperature type (string)",
        {"temperature": "hot", "humidity": 60},
        400
    )

    # Temperature out of range (too low)
    test_case(
        "Temperature too low",
        {"temperature": -50, "humidity": 60},
        400
    )

    # Temperature out of range (too high)
    test_case(
        "Temperature too high",
        {"temperature": 100, "humidity": 60},
        400
    )

    # Humidity out of range (negative)
    test_case(
        "Humidity negative",
        {"temperature": 23.5, "humidity": -10},
        400
    )

    # Humidity out of range (too high)
    test_case(
        "Humidity too high",
        {"temperature": 23.5, "humidity": 150},
        400
    )

    # Edge cases (valid)
    test_case(
        "Temperature minimum edge (-40)",
        {"temperature": -40, "humidity": 50},
        200
    )

    test_case(
        "Temperature maximum edge (85)",
        {"temperature": 85, "humidity": 50},
        200
    )

    test_case(
        "Humidity minimum edge (0)",
        {"temperature": 20, "humidity": 0},
        200
    )

    test_case(
        "Humidity maximum edge (100)",
        {"temperature": 20, "humidity": 100},
        200
    )

    print("\n" + "="*60)
    print("Testing complete!")
    print("\nCheck server logs for validation messages.")
