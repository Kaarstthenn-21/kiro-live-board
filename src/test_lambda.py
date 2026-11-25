"""
Simple local test for Lambda handler logic
Tests validation and routing without DynamoDB
"""

import json
import sys
sys.path.insert(0, '.')

from app import (
    validate_registration_data,
    extract_first_name,
    restore_interest_case,
    create_response
)


def test_validation():
    """Test registration data validation"""
    print("Testing validation...")
    
    # Valid data
    valid_data = {
        'name': 'Juan Pérez García',
        'email': 'juan.perez@company.com',
        'company': 'Acme Corp',
        'role': 'Software Engineer',
        'interest': 'AI & Machine Learning',
        'consent': True
    }
    is_valid, error = validate_registration_data(valid_data)
    assert is_valid, f"Valid data failed: {error}"
    print("✓ Valid data accepted")
    
    # Missing field
    invalid_data = valid_data.copy()
    del invalid_data['consent']
    is_valid, error = validate_registration_data(invalid_data)
    assert not is_valid, "Should reject missing consent"
    assert 'consent' in error, f"Error should mention consent: {error}"
    print("✓ Missing field rejected")
    
    # Invalid email
    invalid_data = valid_data.copy()
    invalid_data['email'] = 'not-an-email'
    is_valid, error = validate_registration_data(invalid_data)
    assert not is_valid, "Should reject invalid email"
    assert 'email' in error.lower(), f"Error should mention email: {error}"
    print("✓ Invalid email rejected")
    
    # Invalid interest
    invalid_data = valid_data.copy()
    invalid_data['interest'] = 'Invalid Interest'
    is_valid, error = validate_registration_data(invalid_data)
    assert not is_valid, "Should reject invalid interest"
    assert 'interest' in error.lower(), f"Error should mention interest: {error}"
    print("✓ Invalid interest rejected")
    
    # Case-insensitive interest
    case_variant = valid_data.copy()
    case_variant['interest'] = 'ai & MACHINE learning'
    is_valid, error = validate_registration_data(case_variant)
    assert is_valid, f"Should accept case-insensitive interest: {error}"
    print("✓ Case-insensitive interest accepted")
    
    # Consent must be true
    invalid_data = valid_data.copy()
    invalid_data['consent'] = False
    is_valid, error = validate_registration_data(invalid_data)
    assert not is_valid, "Should reject consent=false"
    print("✓ Consent=false rejected")


def test_first_name_extraction():
    """Test first name extraction logic"""
    print("\nTesting first name extraction...")
    
    test_cases = [
        ('Juan Pérez García', 'Juan'),
        ('María', 'María'),
        ('José Luis Rodríguez', 'José'),
        ('  Spaced Name  ', 'Spaced'),
        ('', ''),
        ('Single', 'Single')
    ]
    
    for full_name, expected_first in test_cases:
        result = extract_first_name(full_name)
        assert result == expected_first, f"Failed for '{full_name}': got '{result}', expected '{expected_first}'"
        print(f"✓ '{full_name}' -> '{result}'")


def test_interest_case_restoration():
    """Test interest case restoration"""
    print("\nTesting interest case restoration...")
    
    test_cases = [
        ('ai & machine learning', 'AI & Machine Learning'),
        ('cloud architecture', 'Cloud Architecture'),
        ('devops & automation', 'DevOps & Automation'),
        ('security', 'Security'),
        ('data engineering', 'Data Engineering'),
        ('other', 'Other')
    ]
    
    for lowercase, expected in test_cases:
        result = restore_interest_case(lowercase)
        assert result == expected, f"Failed for '{lowercase}': got '{result}', expected '{expected}'"
        print(f"✓ '{lowercase}' -> '{result}'")


def test_response_format():
    """Test response creation"""
    print("\nTesting response format...")
    
    response = create_response(200, {'message': 'Success', 'data': 123})
    
    assert response['statusCode'] == 200
    assert 'headers' in response
    assert response['headers']['Content-Type'] == 'application/json'
    assert 'Access-Control-Allow-Origin' in response['headers']
    
    body = json.loads(response['body'])
    assert body['message'] == 'Success'
    assert body['data'] == 123
    
    print("✓ Response format correct")
    print(f"  Status: {response['statusCode']}")
    print(f"  Headers: {response['headers']}")
    print(f"  Body: {response['body']}")


if __name__ == '__main__':
    try:
        test_validation()
        test_first_name_extraction()
        test_interest_case_restoration()
        test_response_format()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
