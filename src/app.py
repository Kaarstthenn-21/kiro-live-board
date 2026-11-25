"""
Kiro Live Board Lambda Handler

Handles attendee registration and live board data aggregation for the
Kiro Live Board serverless event registration system.

Routes:
- POST /register: Register new attendees with duplicate email prevention
- GET /board: Retrieve aggregated statistics and recent attendees for dashboard
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Tuple
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Environment variables
TABLE_NAME = os.environ.get('TABLE_NAME', 'KiroLiveBoardAttendees')
GSI_NAME = os.environ.get('GSI_NAME', 'TimestampIndex')

# Valid interest categories (case-insensitive matching)
VALID_INTERESTS = {
    'ai & machine learning',
    'cloud architecture',
    'devops & automation',
    'security',
    'data engineering',
    'other'
}

# Email validation regex (basic RFC 5322 compliant pattern)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Entry point for all API requests.
    Routes based on HTTP method and path.
    
    Args:
        event: API Gateway Lambda proxy integration event
        context: Lambda context object
    
    Returns:
        API Gateway Lambda proxy integration response with statusCode, headers, and body
    """
    try:
        # Extract HTTP method and path from event
        route_key = event.get('routeKey', '')
        
        # Route to appropriate handler
        if route_key == 'POST /register':
            return handle_registration(event)
        elif route_key == 'GET /board':
            return handle_board_data()
        else:
            return create_response(404, {
                'error': 'Not Found',
                'message': f'Route not found: {route_key}'
            })
    
    except Exception as e:
        # Catch all unexpected errors
        print(f'Unexpected error: {str(e)}')
        return create_response(500, {
            'error': 'Internal Server Error',
            'message': 'An error occurred processing your request'
        })


def handle_registration(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle POST /register endpoint.
    Validates registration data and writes to DynamoDB with duplicate prevention.
    
    Args:
        event: API Gateway event containing registration data in body
    
    Returns:
        Response with 200 (success), 409 (duplicate), 400 (invalid), or 500 (error)
    """
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields and data format
        is_valid, error_message = validate_registration_data(body)
        if not is_valid:
            return create_response(400, {
                'error': 'Bad Request',
                'message': error_message
            })
        
        # Extract and normalize data
        email = body['email'].strip().lower()
        name = body['name'].strip()
        company = body['company'].strip()
        role = body['role'].strip()
        interest = body['interest'].strip()
        consent = body['consent']
        
        # Generate ISO 8601 timestamp
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Attempt to write to DynamoDB with conditional expression
        try:
            dynamodb.put_item(
                TableName=TABLE_NAME,
                Item={
                    'email': {'S': email},
                    'name': {'S': name},
                    'company': {'S': company},
                    'role': {'S': role},
                    'interest': {'S': interest},
                    'consent': {'BOOL': consent},
                    'timestamp': {'S': timestamp},
                    'gsiPK': {'S': 'BOARD'}  # Constant partition key for GSI
                },
                ConditionExpression='attribute_not_exists(email)'
            )
            
            # Success - new registration created
            return create_response(200, {
                'message': 'Registration successful',
                'attendeeId': email
            })
        
        except ClientError as e:
            # Check if error is due to duplicate email
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return create_response(409, {
                    'error': 'Conflict',
                    'message': 'Email already registered'
                })
            else:
                # Other DynamoDB errors
                print(f'DynamoDB error: {str(e)}')
                raise
    
    except json.JSONDecodeError:
        return create_response(400, {
            'error': 'Bad Request',
            'message': 'Invalid JSON in request body'
        })
    
    except Exception as e:
        print(f'Registration error: {str(e)}')
        return create_response(500, {
            'error': 'Internal Server Error',
            'message': 'An error occurred processing your request'
        })


def handle_board_data() -> Dict[str, Any]:
    """
    Handle GET /board endpoint.
    Retrieves aggregated statistics and recent attendees from DynamoDB.
    
    Returns:
        Response with board data including totalCount, interestBreakdown, and recentAttendees
    """
    try:
        # Scan table for total count and interest aggregation
        total_count, interest_breakdown = aggregate_attendee_statistics()
        
        # Query GSI for 12 most recent attendees
        recent_attendees = get_recent_attendees()
        
        # Return aggregated board data
        return create_response(200, {
            'totalCount': total_count,
            'interestBreakdown': interest_breakdown,
            'recentAttendees': recent_attendees
        })
    
    except Exception as e:
        print(f'Board data error: {str(e)}')
        return create_response(500, {
            'error': 'Internal Server Error',
            'message': 'An error occurred processing your request'
        })


def validate_registration_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate registration data structure and content.
    
    Args:
        data: Registration data dictionary from request body
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = ['name', 'email', 'company', 'role', 'interest', 'consent']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate email format
    email = data['email'].strip()
    if not EMAIL_REGEX.match(email):
        return False, 'Invalid email format'
    
    # Validate consent is true (not just present)
    if data['consent'] is not True:
        return False, 'Consent must be accepted'
    
    # Validate interest is from allowed list (case-insensitive)
    interest = data['interest'].strip().lower()
    if interest not in VALID_INTERESTS:
        return False, f"Invalid interest value. Must be one of: {', '.join(sorted(VALID_INTERESTS))}"
    
    # Validate non-empty strings for text fields
    if not data['name'].strip():
        return False, 'Name cannot be empty'
    if not data['company'].strip():
        return False, 'Company cannot be empty'
    if not data['role'].strip():
        return False, 'Role cannot be empty'
    
    return True, ''


def aggregate_attendee_statistics() -> Tuple[int, List[Dict[str, Any]]]:
    """
    Scan DynamoDB table to get total count and interest breakdown.
    
    Returns:
        Tuple of (total_count, interest_breakdown_list)
    """
    interest_counts = {}
    total_count = 0
    
    # Scan table (paginate if needed)
    scan_kwargs = {
        'TableName': TABLE_NAME,
        'ProjectionExpression': 'interest'
    }
    
    while True:
        response = dynamodb.scan(**scan_kwargs)
        
        # Count items by interest (case-insensitive aggregation)
        for item in response.get('Items', []):
            if 'interest' in item and 'S' in item['interest']:
                interest = item['interest']['S'].strip()
                # Normalize to title case for consistent display
                interest_key = interest.lower()
                if interest_key in interest_counts:
                    interest_counts[interest_key] += 1
                else:
                    interest_counts[interest_key] = 1
                total_count += 1
        
        # Check if more pages exist
        if 'LastEvaluatedKey' not in response:
            break
        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
    
    # Format interest breakdown for response (restore proper capitalization)
    interest_breakdown = [
        {
            'interest': restore_interest_case(interest),
            'count': count
        }
        for interest, count in interest_counts.items()
    ]
    
    # Sort by count descending for better visualization
    interest_breakdown.sort(key=lambda x: x['count'], reverse=True)
    
    return total_count, interest_breakdown


def get_recent_attendees() -> List[Dict[str, Any]]:
    """
    Query GSI to get 12 most recent attendees ordered by timestamp descending.
    Extracts first name and company only (privacy protection).
    
    Returns:
        List of recent attendee dictionaries with firstName, company, timestamp
    """
    try:
        # Query GSI with constant partition key and descending timestamp sort
        response = dynamodb.query(
            TableName=TABLE_NAME,
            IndexName=GSI_NAME,
            KeyConditionExpression='gsiPK = :pk',
            ExpressionAttributeValues={
                ':pk': {'S': 'BOARD'}
            },
            ScanIndexForward=False,  # Descending order (most recent first)
            Limit=12,
            ProjectionExpression='#n, company, #t',
            ExpressionAttributeNames={
                '#n': 'name',  # 'name' is a reserved word in DynamoDB
                '#t': 'timestamp'
            }
        )
        
        # Extract first names and format response
        recent_attendees = []
        for item in response.get('Items', []):
            if 'name' in item and 'company' in item and 'timestamp' in item:
                full_name = item['name']['S']
                first_name = extract_first_name(full_name)
                company = item['company']['S']
                timestamp = item['timestamp']['S']
                
                recent_attendees.append({
                    'firstName': first_name,
                    'company': company,
                    'timestamp': timestamp
                })
        
        return recent_attendees
    
    except Exception as e:
        print(f'Error querying recent attendees: {str(e)}')
        return []


def extract_first_name(full_name: str) -> str:
    """
    Extract first name from full name by splitting on whitespace.
    Handles single-word names by returning the entire name.
    
    Args:
        full_name: Full name string (e.g., "Juan Pérez García")
    
    Returns:
        First name (e.g., "Juan")
    """
    if not full_name:
        return ''
    
    # Split on whitespace and return first token
    parts = full_name.strip().split()
    return parts[0] if parts else ''


def restore_interest_case(interest_lower: str) -> str:
    """
    Restore proper capitalization for interest categories.
    Maps lowercase interest back to display format.
    
    Args:
        interest_lower: Lowercase interest string
    
    Returns:
        Properly capitalized interest string
    """
    # Mapping from lowercase to display format
    case_mapping = {
        'ai & machine learning': 'AI & Machine Learning',
        'cloud architecture': 'Cloud Architecture',
        'devops & automation': 'DevOps & Automation',
        'security': 'Security',
        'data engineering': 'Data Engineering',
        'other': 'Other'
    }
    
    return case_mapping.get(interest_lower, interest_lower.title())


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create standardized API Gateway response with JSON content type.
    
    Args:
        status_code: HTTP status code
        body: Response body dictionary (will be JSON serialized)
    
    Returns:
        API Gateway Lambda proxy integration response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }
