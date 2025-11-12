# Komfyrvakt API Documentation

Complete API reference for Komfyrvakt logging service.

## Base URL

**Local:** `http://localhost:8080`  
**Production:** TBD (after deployment)

## Authentication

All endpoints (except `/` and `/health`) require API key authentication.

**Header:**
```
Authorization: Bearer kmf_your_api_key_here
```

**Getting Your API Key:**
- Auto-generated on first run and saved to `.env` file
- Set via environment variable: `KOMFYRVAKT_API_KEY`
- Displayed in terminal on first startup

**Error Response (401):**
```json
{
  "detail": "Invalid API key"
}
```

---

## Endpoints

### Health & Info

#### `GET /`

Root endpoint with service information.

**No authentication required.**

**Response:**
```json
{
  "service": "Komfyrvakt",
  "version": "0.1.0",
  "description": "Simple logging service with AI analytics",
  "tagline": "Preventing infrastructure fires 🔥"
}
```

#### `GET /health`

Health check endpoint.

**No authentication required.**

**Response:**
```json
{
  "status": "healthy",
  "service": "Komfyrvakt"
}
```

---

### Log Ingestion

#### `POST /logs`

Ingest a single log entry.

**Authentication:** Required

**Request Body:**
```json
{
  "message": "Temperature reading",
  "level": "info",
  "group": "restaurant-a:fridge-1",
  "tags": ["temperature", "monitoring"],
  "data": {
    "temperature": 4.2,
    "humidity": 65
  },
  "timestamp": "2025-11-12T20:15:30Z",
  "source": "sensor-temp-001"
}
```

**Fields:**
- `message` (required, string) - Log message
- `level` (optional, string) - Log level: `debug`, `info`, `warning`, `error`, `critical` (default: `info`)
- `group` (optional, string) - Group identifier for organization (e.g., `service:api`, `project:obsero:prod`, `tenant-123:sensor-456`)
- `tags` (optional, array) - Tags for filtering (default: `[]`)
- `data` (optional, object) - Additional structured data
- `timestamp` (optional, ISO 8601) - Log timestamp (auto-generated if not provided)
- `source` (optional, string) - Source identifier (e.g., sensor ID, service name)

**Response (200):**
```json
{
  "id": "log_20251112201530_abc123",
  "message": "Temperature reading",
  "level": "info",
  "group": "restaurant-a:fridge-1",
  "tags": ["temperature", "monitoring"],
  "data": {
    "temperature": 4.2,
    "humidity": 65
  },
  "timestamp": "2025-11-12T20:15:30Z",
  "source": "sensor-temp-001"
}
```

**Example (PowerShell):**
```powershell
$headers = @{
    "Authorization" = "Bearer kmf_your_api_key"
    "Content-Type" = "application/json"
}

$body = @{
    message = "Temperature too high"
    level = "warning"
    group = "restaurant-a:fridge-1"
    tags = @("temperature", "critical")
    data = @{
        temperature = 8.5
        threshold = 6.0
    }
} | ConvertTo-Json

Invoke-WebRequest -Method POST -Uri "http://localhost:8081/logs" -Headers $headers -Body $body
```

**Example (curl):**
```bash
curl -X POST "http://localhost:8081/logs" \
  -H "Authorization: Bearer kmf_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Temperature too high",
    "level": "warning",
    "tags": ["fridge-1", "critical"],
    "data": {"temperature": 8.5}
  }'
```

**Example (Python):**
```python
import requests

headers = {"Authorization": "Bearer kmf_your_api_key"}
log_data = {
    "message": "Temperature too high",
    "level": "warning",
    "tags": ["fridge-1", "critical"],
    "data": {"temperature": 8.5}
}

response = requests.post(
    "http://localhost:8081/logs",
    headers=headers,
    json=log_data
)
print(response.json())
```

---

### Log Querying

#### `GET /logs`

Query logs with optional filters.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `group` | string | Filter by group (exact or prefix with *) | `restaurant-a:fridge-1` or `restaurant-a:*` |
| `tags` | string | Comma-separated tags (OR logic) | `fridge-1,fridge-2` |
| `level` | string | Minimum log level filter | `warning` |
| `since` | ISO 8601 | Logs after this timestamp | `2025-11-12T00:00:00Z` |
| `until` | ISO 8601 | Logs before this timestamp | `2025-11-12T23:59:59Z` |
| `source` | string | Filter by source identifier | `sensor-001` |
| `limit` | integer | Max results (1-1000, default: 100) | `50` |

**Response (200):**
```json
[
  {
    "id": "log_20251112201530_abc123",
    "message": "Temperature too high",
    "level": "warning",
    "tags": ["fridge-1", "critical"],
    "data": {"temperature": 8.5},
    "timestamp": "2025-11-12T20:15:30Z",
    "source": "sensor-temp-001"
  },
  {
    "id": "log_20251112201520_def456",
    "message": "Temperature normal",
    "level": "info",
    "tags": ["fridge-1"],
    "data": {"temperature": 4.2},
    "timestamp": "2025-11-12T20:15:20Z",
    "source": "sensor-temp-001"
  }
]
```

**Examples:**

Get all logs for a group:
```
GET /logs?group=restaurant-a:fridge-1
```

Get all logs for a group prefix:
```
GET /logs?group=restaurant-a:*
GET /logs?group=service:api:*
```

Get all warning and error logs:
```
GET /logs?level=warning&limit=50
```

Get logs for specific tag:
```
GET /logs?tags=temperature,humidity
```

Get logs in time range:
```
GET /logs?since=2025-11-12T00:00:00Z&until=2025-11-12T23:59:59Z
```

Get logs from specific source:
```
GET /logs?source=sensor-temp-001
```

Combine filters:
```
GET /logs?group=restaurant-a:*&level=error&limit=10
GET /logs?tags=temperature&level=warning&since=2025-11-12T00:00:00Z
```

**PowerShell Example:**
```powershell
$headers = @{"Authorization" = "Bearer kmf_your_api_key"}
Invoke-WebRequest -Uri "http://localhost:8081/logs?tags=fridge-1&level=warning" -Headers $headers
```

**curl Example:**
```bash
curl "http://localhost:8081/logs?tags=fridge-1&level=warning&limit=20" \
  -H "Authorization: Bearer kmf_your_api_key"
```

---

#### `GET /logs/{log_id}`

Get a specific log by its ID.

**Authentication:** Required

**Path Parameter:**
- `log_id` - Log ID (e.g., `log_20251112201530_abc123`)

**Response (200):**
```json
{
  "id": "log_20251112201530_abc123",
  "message": "Temperature too high",
  "level": "warning",
  "tags": ["fridge-1"],
  "data": {"temperature": 8.5},
  "timestamp": "2025-11-12T20:15:30Z",
  "source": "sensor-temp-001"
}
```

**Response (404):**
```json
{
  "detail": "Log log_xyz not found"
}
```

**Example:**
```bash
GET /logs/log_20251112201530_abc123
Authorization: Bearer kmf_your_api_key
```

---

### Statistics

#### `GET /stats`

Get platform statistics.

**Authentication:** Required

**Response (200):**
```json
{
  "status": "success",
  "stats": {
    "total_logs": 1247,
    "storage": "redis",
    "retention_hours": 48
  }
}
```

**Example:**
```powershell
$headers = @{"Authorization" = "Bearer kmf_your_api_key"}
Invoke-WebRequest -Uri "http://localhost:8081/stats" -Headers $headers
```

---

### Purge Logs

#### `DELETE /purge`

Purge logs from storage. Can purge all logs or filter by group.

**Authentication:** Required

⚠️ **Warning:** This operation cannot be undone!

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `group` | string | Group to purge (omit to purge ALL logs) | `restaurant-a:fridge-1` or `restaurant-a:*` |

**Response (200):**

Purge specific group:
```json
{
  "status": "success",
  "result": {
    "purged": 42,
    "group": "restaurant-a:*",
    "scope": "group"
  }
}
```

Purge all logs:
```json
{
  "status": "success",
  "result": {
    "purged": 1247,
    "indexes_cleared": 3562,
    "scope": "all"
  }
}
```

**Examples:**

Purge specific group:
```
DELETE /purge?group=restaurant-a:fridge-1
```

Purge all logs in a prefix:
```
DELETE /purge?group=restaurant-a:*
DELETE /purge?group=service:api:*
```

Purge ALL logs (dangerous!):
```
DELETE /purge
```

**PowerShell Examples:**
```powershell
$headers = @{"Authorization" = "Bearer kmf_your_api_key"}

# Purge specific group
Invoke-WebRequest -Method DELETE -Uri "http://localhost:8081/purge?group=test-group" -Headers $headers

# Purge ALL (⚠️ careful!)
Invoke-WebRequest -Method DELETE -Uri "http://localhost:8081/purge" -Headers $headers
```

**cURL Examples:**
```bash
# Purge specific group
curl -X DELETE "http://localhost:8081/purge?group=restaurant-a:fridge-1" \
  -H "Authorization: Bearer kmf_your_key"

# Purge group prefix
curl -X DELETE "http://localhost:8081/purge?group=restaurant-a:*" \
  -H "Authorization: Bearer kmf_your_key"

# Purge ALL
curl -X DELETE "http://localhost:8081/purge" \
  -H "Authorization: Bearer kmf_your_key"
```

---

## Data Models

### LogEntry (Input)

```typescript
{
  message: string;           // Required
  level?: "debug" | "info" | "warning" | "error" | "critical";  // Default: "info"
  group?: string;            // Group identifier (e.g., "service:api", "tenant-123:sensor-456")
  tags?: string[];           // Default: []
  data?: object;             // Any JSON object
  timestamp?: string;        // ISO 8601, auto-generated if omitted
  source?: string;           // Optional source identifier
}
```

### StoredLog (Output)

```typescript
{
  id: string;                // Auto-generated, format: log_YYYYMMDDHHmmss_xxxxxxxx
  message: string;
  level: "debug" | "info" | "warning" | "error" | "critical";
  group?: string;            // Group identifier
  tags: string[];
  data?: object;
  timestamp: string;         // ISO 8601
  source?: string;
}
```

### Log Levels (Priority Order)

1. `debug` - Lowest priority, verbose information
2. `info` - General informational messages
3. `warning` - Warning messages, potential issues
4. `error` - Error conditions
5. `critical` - Highest priority, critical failures

When filtering by level (e.g., `?level=warning`), returns logs at that level **and above** (warning, error, critical).

---

## Redis Storage

### Key Structure

**Log entries:**
```
komfyrvakt:logs:{log_id}
```

**Tag indexes:**
```
komfyrvakt:index:tag:{tag}:{log_id}
```

### TTL (Time to Live)

- Default: 48 hours
- Configurable via `LOG_RETENTION_HOURS` environment variable
- Logs automatically expire after retention period

### Key Namespacing

All logs are namespaced with `komfyrvakt:` prefix to avoid collisions with other services using the same Redis instance.

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KOMFYRVAKT_API_KEY` | Auto-generated | API key for authentication |
| `REDIS_HOST` | `localhost` | Redis server hostname |
| `REDIS_PORT` | `6379` | Redis server port |
| `ENVIRONMENT` | `local` | Environment (`local` or `production`) |
| `LOG_RETENTION_HOURS` | `48` | How long to keep logs in Redis |
| `COLD_STORAGE` | `none` | Cold storage backend (`none`, `gcs`, `firestore`) |
| `AI_PROVIDER` | `none` | AI provider (`none`, `gemini`, `openai`) |
| `PORT` | `8080` | Server port |

### .env File

Create `.env` file in project root:

```bash
KOMFYRVAKT_API_KEY=kmf_your_key_here
REDIS_HOST=34.66.188.104
REDIS_PORT=6379
ENVIRONMENT=local
LOG_RETENTION_HOURS=48
```

Or let it auto-generate on first run!

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid API key"
}
```

Missing or invalid Authorization header.

### 404 Not Found
```json
{
  "detail": "Log log_xyz not found"
}
```

Requested log ID doesn't exist or has expired.

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "message"],
      "msg": "Input should be a valid string"
    }
  ]
}
```

Request body doesn't match expected schema.

### 500 Internal Server Error
```json
{
  "detail": "Failed to store log: connection error"
}
```

Server-side error (Redis connection, etc.)

---

## Rate Limits

Currently no rate limiting implemented.

**Future:** Rate limiting per API key based on plan/tier.

---

## Interactive API Docs

Visit `/docs` for interactive Swagger UI documentation where you can:
- Test all endpoints
- See request/response schemas
- Try different filters
- Authenticate with your API key

Visit `/redoc` for alternative ReDoc documentation.

---

## Client Examples

### Python Client

```python
import requests
from datetime import datetime

class KomfyrvaktClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def log(self, message: str, level: str = "info", tags: list = None, data: dict = None):
        response = requests.post(
            f"{self.base_url}/logs",
            headers=self.headers,
            json={
                "message": message,
                "level": level,
                "tags": tags or [],
                "data": data
            }
        )
        return response.json()
    
    def query(self, tags: list = None, level: str = None, limit: int = 100):
        params = {"limit": limit}
        if tags:
            params["tags"] = ",".join(tags)
        if level:
            params["level"] = level
        
        response = requests.get(
            f"{self.base_url}/logs",
            headers=self.headers,
            params=params
        )
        return response.json()

# Usage
client = KomfyrvaktClient("http://localhost:8081", "kmf_your_key")
client.log("Server started", level="info", tags=["api", "startup"])
logs = client.query(tags=["api"], level="warning")
```

### JavaScript/TypeScript Client

```typescript
class KomfyrvaktClient {
  constructor(private baseUrl: string, private apiKey: string) {}

  async log(params: {
    message: string;
    level?: 'debug' | 'info' | 'warning' | 'error' | 'critical';
    tags?: string[];
    data?: Record<string, any>;
    source?: string;
  }) {
    const response = await fetch(`${this.baseUrl}/logs`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        level: 'info',
        tags: [],
        ...params
      })
    });
    return response.json();
  }

  async query(params?: {
    tags?: string[];
    level?: string;
    since?: string;
    until?: string;
    source?: string;
    limit?: number;
  }) {
    const searchParams = new URLSearchParams();
    if (params?.tags) searchParams.set('tags', params.tags.join(','));
    if (params?.level) searchParams.set('level', params.level);
    if (params?.since) searchParams.set('since', params.since);
    if (params?.until) searchParams.set('until', params.until);
    if (params?.source) searchParams.set('source', params.source);
    if (params?.limit) searchParams.set('limit', params.limit.toString());

    const response = await fetch(
      `${this.baseUrl}/logs?${searchParams}`,
      {
        headers: { 'Authorization': `Bearer ${this.apiKey}` }
      }
    );
    return response.json();
  }
}

// Usage
const client = new KomfyrvaktClient('http://localhost:8081', 'kmf_your_key');
await client.log({
  message: 'User login',
  level: 'info',
  tags: ['auth', 'user-123'],
  data: { ip: '192.168.1.1' }
});

const logs = await client.query({ tags: ['auth'], level: 'error' });
```

### cURL Examples

**POST log:**
```bash
curl -X POST "http://localhost:8081/logs" \
  -H "Authorization: Bearer kmf_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Database query slow",
    "level": "warning",
    "tags": ["database", "performance"],
    "data": {"duration_ms": 1523, "query": "SELECT * FROM users"}
  }'
```

**Query logs:**
```bash
curl "http://localhost:8081/logs?tags=database&level=warning" \
  -H "Authorization: Bearer kmf_your_key"
```

**Get specific log:**
```bash
curl "http://localhost:8081/logs/log_20251112201530_abc123" \
  -H "Authorization: Bearer kmf_your_key"
```

**Get stats:**
```bash
curl "http://localhost:8081/stats" \
  -H "Authorization: Bearer kmf_your_key"
```

---

## Groups vs Tags

**Groups** - Primary organization (hierarchical, queryable with prefix):
- `"service:api"` - All API logs
- `"project:obsero:prod"` - Production Obsero logs
- `"tenant-123:sensor-temp-001"` - Specific sensor logs
- `"restaurant-a:fridge-1"` - Restaurant's fridge logs

**Tags** - Secondary filtering (flat, OR logic):
- `["temperature", "monitoring"]`
- `["error", "critical", "needs-attention"]`
- `["production", "europe"]`

**Example:**
```json
{
  "message": "High temperature detected",
  "group": "restaurant-a:fridge-1",
  "tags": ["temperature", "alert", "critical"]
}
```

Query all restaurant-a logs: `?group=restaurant-a:*`  
Query critical logs: `?tags=critical`  
Query restaurant-a critical logs: `?group=restaurant-a:*&tags=critical`

---

## Common Use Cases

### Application Logging

```python
# In your application
from komfyrvakt_client import KomfyrvaktClient

logger = KomfyrvaktClient("https://komfyrvakt.example.com", "kmf_your_key")

# Log events with groups
logger.log(
    "User registered", 
    level="info", 
    group="service:auth:prod",
    tags=["user", "registration"], 
    data={"user_id": "123", "email": "user@example.com"}
)

logger.log(
    "Payment failed", 
    level="error",
    group="service:payment:prod",
    tags=["stripe", "critical"],
    data={"amount": 99.99, "error": "Card declined"}
)
```

### IoT Sensor Data

```python
# Temperature sensor posting every 10 seconds
sensor_id = "sensor-temp-fridge1"
restaurant_id = "restaurant-a"

while True:
    temp = read_temperature()
    
    level = "warning" if temp > 6.0 else "info"
    logger.log(
        f"Temperature: {temp}°C",
        level=level,
        group=f"{restaurant_id}:fridge-1",
        tags=["temperature", "monitoring"],
        data={"temperature": temp, "threshold": 6.0},
        source=sensor_id
    )
    
    time.sleep(10)

# Later, query all logs for this restaurant:
# GET /logs?group=restaurant-a:*
```

### Error Tracking

```python
try:
    result = risky_operation()
except Exception as e:
    logger.log(
        f"Operation failed: {str(e)}",
        level="error",
        tags=["app", "exception", "critical"],
        data={
            "exception_type": type(e).__name__,
            "stack_trace": traceback.format_exc(),
            "context": get_current_context()
        }
    )
```

### Performance Monitoring

```python
import time

start = time.time()
result = api_call()
duration = (time.time() - start) * 1000

level = "warning" if duration > 1000 else "info"
logger.log(
    f"API call completed in {duration:.2f}ms",
    level=level,
    tags=["api", "performance"],
    data={
        "endpoint": "/users/profile",
        "duration_ms": duration,
        "threshold_ms": 1000
    }
)
```

---

## Best Practices

### Group Organization Strategy

Use hierarchical groups for primary organization:

**Recommended patterns:**
```
service:{name}:{env}             # e.g., "service:api:prod"
project:{name}:{env}             # e.g., "project:obsero:staging"
tenant:{id}:{resource}           # e.g., "tenant-123:sensor-456"
app:{name}:{component}           # e.g., "app:dashboard:frontend"
{custom}:{hierarchy}:{you-want} # Any structure works!
```

**Examples:**
```json
{"group": "service:api:prod"}                    // Production API logs
{"group": "project:obsero:dev"}                  // Obsero dev logs
{"group": "restaurant-a:fridge-1"}               // Restaurant's fridge
{"group": "iot:building-5:floor-2:sensor-temp"}  // Nested IoT hierarchy
```

**Query flexibility:**
```
?group=restaurant-a:*              // All restaurant-a logs
?group=service:api:*               // All API logs (prod + staging)
?group=iot:building-5:*            // All building-5 sensors
```

### Tagging Strategy

Use tags for cross-cutting concerns:

**Good tags:**
- Status: `critical`, `needs-attention`, `resolved`
- Type: `temperature`, `humidity`, `performance`, `error`
- Category: `monitoring`, `alert`, `audit`
- Priority: `high`, `medium`, `low`

**Example:**
```json
{
  "message": "Database query slow",
  "group": "service:api:prod",
  "tags": ["performance", "database", "needs-optimization"]
}
```

**Why this is better:**
- **Group** = Where (service, tenant, resource)
- **Tags** = What (type, category, status)

Query all critical issues across all services: `?tags=critical`  
Query all API performance issues: `?group=service:api:*&tags=performance`

### Data Structure

Keep `data` field structured and consistent:

**Good:**
```json
{
  "data": {
    "duration_ms": 1523,
    "endpoint": "/api/users",
    "status_code": 200
  }
}
```

**Bad:**
```json
{
  "data": "duration: 1523ms, endpoint: /api/users, status: 200"
}
```

Structured data enables better AI analysis and querying.

### Log Levels

**debug:** Development-only, verbose details  
**info:** Normal operations, successful events  
**warning:** Unexpected but handled, degraded performance  
**error:** Errors that need attention  
**critical:** System failures, immediate action required  

Use appropriate levels for better filtering and alerting.

---

## Future Endpoints (Planned)

### Batch Ingestion
```
POST /logs/batch
```

Submit multiple logs in one request (more efficient).

### AI Analytics
```
GET /analytics/report?tags=fridge-1&hours=24
POST /analytics/detect-anomalies
```

AI-powered insights and anomaly detection.

### Admin
```
POST /admin/regenerate-key
GET /admin/metrics
```

Administrative operations (requires admin secret).

---

## Support

For issues or questions:
- Check `/docs` for interactive API documentation
- Review examples in this documentation
- See main README for architecture details

