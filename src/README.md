# Lambda Function Implementation

## Overview

The `app.py` Lambda function handler implements the backend API for the Kiro Live Board serverless event registration system. It handles two primary routes:

- **POST /register**: Register new event attendees with duplicate email prevention
- **GET /board**: Retrieve aggregated statistics and recent attendees for the live dashboard

## Architecture

### Request Flow

```
API Gateway HTTP API
    ↓
Lambda Handler (app.lambda_handler)
    ↓
Route Dispatcher (POST /register or GET /board)
    ↓
├─ handle_registration()           ├─ handle_board_data()
   ├─ validate_registration_data()    ├─ aggregate_attendee_statistics()
   ├─ DynamoDB PutItem (conditional)  └─ get_recent_attendees()
   └─ Return 200/409/400                 └─ extract_first_name()
```

## Key Functions

### `lambda_handler(event, context)`
Entry point for all API requests. Routes based on `routeKey` from API Gateway.

**Returns:**
- Routes to `handle_registration()` for POST /register
- Routes to `handle_board_data()` for GET /board
- Returns 404 for unknown routes
- Returns 500 for unexpected errors

### `handle_registration(event)`
Processes attendee registration requests.

**Validation:**
- Required fields: name, email, company, role, interest, consent
- Email format validation using RFC 5322 regex
- Interest must be from predefined list (case-insensitive)
- Consent must be `true`

**DynamoDB Write:**
- Uses conditional `PutItem` with `attribute_not_exists(email)`
- Adds server-generated timestamp in ISO 8601 format
- Adds constant `gsiPK = "BOARD"` for GSI queries

**Responses:**
- **200**: Registration successful
- **409**: Email already registered (ConditionalCheckFailedException)
- **400**: Invalid data (missing fields, bad email, invalid interest)
- **500**: Server error

### `handle_board_data()`
Retrieves aggregated data for the live dashboard.

**Operations:**
1. **Scan Table**: Count total attendees and aggregate by interest
2. **Query GSI**: Get 12 most recent attendees (descending timestamp)

**Data Processing:**
- Extracts first names only (privacy protection)
- Normalizes interest categories (case-insensitive aggregation)
- Never includes email addresses in response

**Response Format:**
```json
{
  "totalCount": 47,
  "interestBreakdown": [
    {"interest": "AI & Machine Learning", "count": 15},
    {"interest": "Cloud Architecture", "count": 12}
  ],
  "recentAttendees": [
    {"firstName": "Juan", "company": "Acme Corp", "timestamp": "2025-01-15T10:30:45Z"}
  ]
}
```

### `validate_registration_data(data)`
Validates registration payload structure and content.

**Checks:**
- All required fields present and non-empty
- Email matches regex pattern
- Consent is `true` (not just truthy)
- Interest is from valid list (case-insensitive)

**Returns:** `(is_valid: bool, error_message: str)`

### `extract_first_name(full_name)`
Extracts first name from full name by splitting on whitespace.

**Examples:**
- `"Juan Pérez García"` → `"Juan"`
- `"María"` → `"María"`
- `"José Luis Rodríguez"` → `"José"`

### `aggregate_attendee_statistics()`
Scans DynamoDB table to count total attendees and group by interest.

**Features:**
- Handles pagination automatically
- Case-insensitive interest aggregation
- Sorts breakdown by count (descending)

**Returns:** `(total_count: int, interest_breakdown: List[Dict])`

### `get_recent_attendees()`
Queries GSI to retrieve 12 most recent attendees.

**Query Details:**
- Index: `TimestampIndex`
- Key condition: `gsiPK = "BOARD"`
- Sort: Descending timestamp (`ScanIndexForward=False`)
- Limit: 12 items

**Privacy Protection:**
- Extracts first name only
- Excludes email addresses
- Includes company and timestamp

**Returns:** `List[Dict[str, Any]]` with firstName, company, timestamp

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TABLE_NAME` | DynamoDB table name | `KiroLiveBoardAttendees` |
| `GSI_NAME` | Global Secondary Index name | `TimestampIndex` |

### IAM Permissions Required

- `dynamodb:PutItem` - Write new registrations
- `dynamodb:Scan` - Aggregate statistics
- `dynamodb:Query` - Retrieve recent attendees from GSI
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` - CloudWatch logging

## Interest Categories

Valid interest values (case-insensitive):

1. AI & Machine Learning
2. Cloud Architecture
3. DevOps & Automation
4. Security
5. Data Engineering
6. Other

## Error Handling

### Client Errors (4xx)

**400 Bad Request:**
- Missing required fields
- Invalid email format
- Consent not accepted
- Invalid interest value
- Malformed JSON

**409 Conflict:**
- Email already registered (duplicate)

### Server Errors (5xx)

**500 Internal Server Error:**
- DynamoDB service errors
- Unexpected exceptions
- Lambda execution errors

All errors return JSON with:
```json
{
  "error": "Error Type",
  "message": "Human-readable error message"
}
```

## Testing

### Local Unit Tests

Run validation and logic tests without DynamoDB:

```bash
cd src
python3 test_lambda.py
```

Tests cover:
- Registration data validation
- First name extraction
- Interest case restoration
- Response format

### Local Integration Testing

Use SAM CLI with DynamoDB Local:

```bash
# Start DynamoDB Local (requires Docker)
docker run -p 8000:8000 amazon/dynamodb-local

# Start SAM local API
sam local start-api --env-vars env.json

# Test registration endpoint
curl -X POST http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@company.com",
    "company": "Acme Corp",
    "role": "Engineer",
    "interest": "AI & Machine Learning",
    "consent": true
  }'

# Test board endpoint
curl http://localhost:3000/board
```

### Deployment Testing

After deploying to AWS:

```bash
# Get API URL from stack outputs
sam deploy --guided

# Test live endpoints
API_URL=$(aws cloudformation describe-stacks \
  --stack-name kiro-live-board \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text)

curl -X POST $API_URL/register -H "Content-Type: application/json" -d '{...}'
curl $API_URL/board
```

## Design Requirements Coverage

This implementation validates the following requirements from the design document:

**Registration Requirements:**
- 1.5: Send registration data to API
- 2.1: Check if email exists
- 2.2: Return duplicate status for existing emails
- 2.3: Create new record for new emails
- 2.4: Preserve original data on duplicates

**Board Requirements:**
- 3.2: Display total count
- 3.3: Display bar charts by interest
- 3.4: Display 12 most recent attendees
- 3.6: Never display email addresses
- 3.8: Extract first names only

**Data Requirements:**
- 4.3: Write attendee records to DynamoDB
- 4.4: Query database for board data

**API Requirements:**
- 5.1: POST endpoint for registration
- 5.2: GET endpoint for board data
- 5.3: Invoke Lambda on POST
- 5.4: Invoke Lambda on GET
- 5.5: Return appropriate status codes
- 5.7: Return application/json content type

**Name Processing:**
- 7.1: Extract first name from full name
- 7.2: Split on whitespace
- 7.3: Handle single-word names
- 7.4: Display only first name on board

**Interest Validation:**
- 8.3: Validate interest from predefined list
- 8.4: Group attendees by interest
- 8.5: Display bar charts with labels
- 8.6: Case-insensitive aggregation

## Performance Considerations

- **Cold Start**: ~1-2 seconds for first invocation
- **Warm Execution**: ~100-300ms per request
- **Scan Performance**: O(n) for total count - acceptable for events <10,000 attendees
- **GSI Query**: O(log n + 12) - efficient for recent attendees

For events with >10,000 attendees, consider:
- Using DynamoDB Streams for real-time aggregation
- Caching board data in ElastiCache
- Pre-aggregating counts in separate table

## Security

- **Input Validation**: All inputs validated before database operations
- **SQL Injection**: Not applicable (NoSQL database)
- **CORS**: Configured in API Gateway (allows all origins for public event)
- **Email Privacy**: Emails never exposed in board endpoint
- **Logging**: Errors logged to CloudWatch (excludes sensitive data)

## Maintenance

### Monitoring

Watch CloudWatch metrics:
- `Invocations`: Total Lambda invocations
- `Errors`: Failed executions
- `Duration`: Execution time
- `Throttles`: Rate limit hits

### Logging

CloudWatch Logs include:
- Request routing decisions
- Validation errors
- DynamoDB errors
- Duplicate registration attempts

### Updates

To deploy code changes:

```bash
sam build
sam deploy
```

To rollback:

```bash
aws lambda update-function-code \
  --function-name KiroLiveBoard-RegistrationFunction \
  --s3-bucket previous-deployment-bucket \
  --s3-key previous-version.zip
```
