#!/usr/bin/env python3
"""
Test Program for Microservices
Demonstrates that each microservice can be called and responds with data.
Each test makes HTTP requests to the respective microservice endpoints.
Services are NOT directly calling each other - they communicate via HTTP.
"""

import requests
import json
import sys


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_rating_service():
    """Test the rating-service microservice."""
    print_section("TESTING RATING-SERVICE")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Create/Upsert a rating
        print("Test 1: Upserting a rating...")
        rating_data = {
            "app_id": "book-club",
            "entity_id": "book-123",
            "user_id": "user-456",
            "rating": 5,
            "comment": "Excellent book!"
        }
        
        response = requests.post(f"{base_url}/ratings", json=rating_data)
        print(f"  POST {base_url}/ratings")
        print(f"  Request: {json.dumps(rating_data, indent=2)}")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.status_code != 200:
            print("  ❌ FAILED: Expected 200")
            return False
        print("  ✓ PASSED\n")
        
        # Test 2: Retrieve ratings
        print("Test 2: Retrieving ratings...")
        response = requests.get(
            f"{base_url}/ratings",
            params={
                "app_id": "book-club",
                "entity_id": "book-123"
            }
        )
        print(f"  GET {base_url}/ratings?app_id=book-club&entity_id=book-123")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.status_code != 200:
            print("  ❌ FAILED: Expected 200")
            return False
        print("  ✓ PASSED\n")
        
        # Test 3: Delete a rating
        print("Test 3: Deleting a rating...")
        response = requests.delete(
            f"{base_url}/ratings",
            params={
                "app_id": "book-club",
                "entity_id": "book-123",
                "user_id": "user-456"
            }
        )
        print(f"  DELETE {base_url}/ratings?app_id=book-club&entity_id=book-123&user_id=user-456")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.status_code != 200:
            print("  ❌ FAILED: Expected 200")
            return False
        print("  ✓ PASSED\n")
        
        print("✓ RATING-SERVICE: All tests passed!")
        return True
        
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ CONNECTION ERROR: Could not connect to rating-service at {base_url}")
        print(f"     Make sure the rating-service is running on port 8000")
        print(f"     Error: {e}\n")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {e}\n")
        return False


def test_ai_prompt_service():
    """Test the ai-prompt-service microservice."""
    print_section("TESTING AI-PROMPT-SERVICE")
    
    base_url = "http://localhost:3000"
    
    try:
        # Test 1: Generate text response
        print("Test 1: Generating text response...")
        prompt_data = {
            "prompt": "What is Python?"
        }
        
        response = requests.post(f"{base_url}/generate", json=prompt_data)
        print(f"  POST {base_url}/generate")
        print(f"  Request: {json.dumps(prompt_data, indent=2)}")
        print(f"  Status Code: {response.status_code}")
        
        response_json = response.json()
        response_preview = str(response_json)[:100] + "..." if len(str(response_json)) > 100 else str(response_json)
        print(f"  Response: {response_preview}")
        
        if response.status_code != 200:
            print("  ❌ FAILED: Expected 200")
            return False
        print("  ✓ PASSED\n")
        
        # Test 2: Generate image response
        print("Test 2: Generating image response...")
        prompt_data = {
            "prompt": "A sunset over mountains"
        }
        
        response = requests.post(f"{base_url}/generate", json=prompt_data)
        print(f"  POST {base_url}/generate")
        print(f"  Request: {json.dumps(prompt_data, indent=2)}")
        print(f"  Status Code: {response.status_code}")
        
        response_json = response.json()
        if "response" in response_json:
            response_preview = f"(Image data, {len(str(response_json['response']))} chars)"
        else:
            response_preview = str(response_json)[:100] + "..." if len(str(response_json)) > 100 else str(response_json)
        print(f"  Response: {response_preview}")
        
        if response.status_code != 200:
            print("  ❌ FAILED: Expected 200")
            return False
        print("  ✓ PASSED\n")
        
        print("✓ AI-PROMPT-SERVICE: All tests passed!")
        return True
        
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ CONNECTION ERROR: Could not connect to ai-prompt-service at {base_url}")
        print(f"     Make sure the ai-prompt-service is running on port 3000")
        print(f"     Error: {e}\n")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {e}\n")
        return False


def test_progress_service():
    """Test the progress-service microservice."""
    print_section("TESTING PROGRESS-SERVICE")

    import requests

    base_url = "http://localhost:5003/progress"

    try:
        response = requests.get(
            base_url,
            params={"userId": "u123", "bookId": "b456"},
            timeout=5
        )

        print("Status Code:", response.status_code)
        print("Raw Response:", response.text)

        # Try to parse JSON
        try:
            data = response.json()
            print("Parsed JSON:", data)
        except Exception:
            print("❌ Could not parse JSON")

        # Determine pass/fail
        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        print("❌ Error contacting Progress Service:", e)
        return False

    

def main():
    """Run all microservice tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  MICROSERVICE TEST PROGRAM".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\nThis test program demonstrates:")
    print("  • Each microservice can be called via HTTP")
    print("  • Each service responds with data")
    print("  • Services communicate via REST API, not direct calls")
    print("  • Multiple services are independently tested\n")
    
    results = {
        "rating-service": test_rating_service(),
        "ai-prompt-service": test_ai_prompt_service(),
        "progress-service": test_progress_service(),
    }
    
    # Print summary
    print_section("TEST SUMMARY")
    
    for service, result in results.items():
        if result is True:
            status = "✓ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⏳ PLACEHOLDER"
        print(f"  {service}: {status}")
    
    # Overall result
    all_passed = all(r is not False for r in results.values() if r is not None)
    
    if all_passed:
        print("\n✓ All active services tested successfully!")
        return 0
    else:
        print("\n❌ Some tests failed. Check service startup.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
