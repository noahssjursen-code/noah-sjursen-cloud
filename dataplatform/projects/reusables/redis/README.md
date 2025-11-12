# Redis Client Library

Production-ready Redis utilities for Noah Sjursen Cloud services.

## Features

- ✅ **Auto-configuration** - Environment-based connection (local/production)
- ✅ **JSON serialization** - Automatic JSON encoding/decoding
- ✅ **Key namespacing** - Prevent collisions between services
- ✅ **TTL management** - Automatic expiration handling
- ✅ **Pattern matching** - Find and invalidate keys by pattern
- ✅ **Bulk operations** - Efficient multi-key operations
- ✅ **Type hints** - Full typing support
- ✅ **Singleton client** - Connection pooling built-in

## Quick Start

```python
from reusables.redis import cache_set, cache_get, get_redis_client

# Simple caching
cache_set('user:123', {'name': 'Noah', 'age': 21}, ttl=3600)
user = cache_get('user:123')

# Direct client access
r = get_redis_client()
r.ping()  # Returns True
```

## Installation

The Redis client is included in the `reusables` library. Install dependencies:

```bash
pip install redis>=5.0.0
```

## Configuration

### Environment Variables

- `ENVIRONMENT` - `local` or `production` (default: `local`)
- `REDIS_HOST` - Override default Redis host
- `REDIS_PORT` - Override Redis port (default: 6379)

### Default Behavior

**Local development:**
- Connects to `34.66.188.104:6379` (external IP)
- For development and testing

**Production (Cloud Run):**
- Connects to `10.128.0.3:6379` (internal VPC IP)
- Set automatically via deploy script

## API Reference

### Core Client

#### `get_redis_client() -> redis.Redis`

Get the shared Redis client singleton.

```python
from reusables.redis import get_redis_client

r = get_redis_client()
r.ping()  # True
```

---

### CRUD Operations

#### `set_value(key: str, value: Any, ttl: Optional[int] = None) -> bool`

Set a value with optional TTL. Complex objects are JSON-serialized automatically.

```python
from reusables.redis import set_value

# String value
set_value('username', 'noah')

# Complex object with TTL
set_value('user:123', {'name': 'Noah', 'age': 21}, ttl=3600)
```

#### `get_value(key: str, default: Any = None) -> Any`

Get a value. JSON objects are automatically deserialized.

```python
from reusables.redis import get_value

user = get_value('user:123')
name = get_value('missing_key', default='Unknown')
```

#### `delete_key(key: str) -> int`

Delete a key. Returns number of keys deleted (0 or 1).

```python
from reusables.redis import delete_key

count = delete_key('user:123')
```

#### `exists(key: str) -> bool`

Check if a key exists.

```python
from reusables.redis import exists

if exists('user:123'):
    print('User exists')
```

#### `get_ttl(key: str) -> int`

Get time-to-live in seconds.

```python
from reusables.redis import get_ttl

ttl = get_ttl('session:abc')
# Returns: seconds remaining, -1 = no expiration, -2 = doesn't exist
```

---

### Bulk Operations

#### `set_many(mapping: Dict[str, Any], ttl: Optional[int] = None) -> bool`

Set multiple key-value pairs at once.

```python
from reusables.redis import set_many

set_many({
    'user:1': {'name': 'Noah'},
    'user:2': {'name': 'Alice'},
    'user:3': {'name': 'Bob'}
}, ttl=3600)
```

#### `get_many(keys: List[str]) -> Dict[str, Any]`

Get multiple values at once. Missing keys are excluded from result.

```python
from reusables.redis import get_many

users = get_many(['user:1', 'user:2', 'user:3'])
# Returns: {'user:1': {...}, 'user:2': {...}, 'user:3': {...}}
```

#### `delete_many(keys: List[str]) -> int`

Delete multiple keys at once. Returns count of deleted keys.

```python
from reusables.redis import delete_many

count = delete_many(['user:1', 'user:2', 'user:3'])
```

---

### Cache Helpers

#### `cache_set(key: str, value: Any, ttl: int = 3600) -> bool`

Set a cached value with default 1-hour TTL.

```python
from reusables.redis import cache_set

# Default 1-hour expiration
cache_set('user:123:profile', user_data)

# Custom TTL (30 minutes)
cache_set('user:123:session', session_data, ttl=1800)
```

#### `cache_get(key: str) -> Optional[Any]`

Get a cached value. Returns `None` if not found.

```python
from reusables.redis import cache_get

profile = cache_get('user:123:profile')
if profile is None:
    profile = fetch_from_database()
    cache_set('user:123:profile', profile)
```

---

### Pattern Matching & Invalidation

#### `find_keys(pattern: str, limit: int = 1000) -> List[str]`

Find keys matching a Redis pattern.

```python
from reusables.redis import find_keys

# Find all user cache keys
user_keys = find_keys('cache:user:*')

# Find specific pattern
session_keys = find_keys('session:user:123:*')
```

**Patterns:**
- `*` matches any characters
- `?` matches single character
- `[abc]` matches a, b, or c

⚠️ **Warning:** Use with caution on large datasets.

#### `invalidate_pattern(pattern: str) -> int`

Delete all keys matching a pattern. Returns count of deleted keys.

```python
from reusables.redis import invalidate_pattern

# Invalidate all cache for a user
count = invalidate_pattern('cache:user:123:*')

# Clear all sessions
count = invalidate_pattern('session:*')
```

⚠️ **Warning:** Scans all keys. Use sparingly in production.

#### `purge_cache(service: Optional[str] = None) -> int`

Purge cache entries for a service or all services.

```python
from reusables.redis import purge_cache

# Purge all FirstApi cache
purge_cache('firstapi')

# Purge all cache across all services
purge_cache()
```

---

### Counters

#### `increment(key: str, amount: int = 1) -> int`

Increment a counter. Returns new value.

```python
from reusables.redis import increment

# Increment by 1
views = increment('page:home:views')

# Increment by custom amount
total = increment('api:requests', amount=10)
```

#### `decrement(key: str, amount: int = 1) -> int`

Decrement a counter. Returns new value.

```python
from reusables.redis import decrement

remaining = decrement('tokens:user:123')
```

**Use cases:**
- Page view counters
- API rate limiting
- Token buckets
- Inventory tracking

---

### Hash Operations

For storing structured data as fields within a single key.

#### `hash_set(key: str, field: str, value: Any) -> int`

Set a field in a hash. Returns 1 if new field, 0 if updated.

```python
from reusables.redis import hash_set

hash_set('user:123', 'name', 'Noah')
hash_set('user:123', 'age', 21)
hash_set('user:123', 'settings', {'theme': 'dark'})
```

#### `hash_get(key: str, field: str) -> Optional[Any]`

Get a field from a hash.

```python
from reusables.redis import hash_get

name = hash_get('user:123', 'name')  # 'Noah'
age = hash_get('user:123', 'age')    # 21
```

#### `hash_get_all(key: str) -> Dict[str, Any]`

Get all fields from a hash as a dictionary.

```python
from reusables.redis import hash_get_all

user = hash_get_all('user:123')
# {'name': 'Noah', 'age': 21, 'settings': {...}}
```

**Use cases:**
- User profiles
- Configuration storage
- Session data
- Object caching

---

### Key Naming

#### `make_key(service: str, *parts: str) -> str`

Create a namespaced key to prevent collisions.

```python
from reusables.redis import make_key

# Create namespaced keys
user_key = make_key('firstapi', 'cache', 'user', '123')
# Returns: 'firstapi:cache:user:123'

session_key = make_key('auth', 'session', 'abc123')
# Returns: 'auth:session:abc123'
```

**Why namespace?**
- Prevents collisions between services
- Easy pattern matching per service
- Clear data ownership
- Easier cache invalidation

**Recommended patterns:**
- `{service}:cache:{resource}:{id}` - Cache entries
- `{service}:session:{session_id}` - Sessions
- `{service}:counter:{name}` - Counters
- `{service}:data:{key}` - General data

---

## Usage Examples

### Simple Caching

```python
from reusables.redis import cache_get, cache_set

def get_user(user_id):
    # Try cache first
    cache_key = f'user:{user_id}'
    user = cache_get(cache_key)
    
    if user is None:
        # Cache miss - fetch from database
        user = database.get_user(user_id)
        cache_set(cache_key, user, ttl=3600)
    
    return user
```

### Rate Limiting

```python
from reusables.redis import increment, get_ttl, set_value

def check_rate_limit(user_id, limit=100):
    key = f'ratelimit:user:{user_id}'
    count = increment(key)
    
    # Set expiration on first request
    if count == 1:
        set_value(key, count, ttl=3600)  # 1 hour window
    
    if count > limit:
        ttl = get_ttl(key)
        raise RateLimitError(f'Try again in {ttl} seconds')
    
    return count
```

### Page View Counter

```python
from reusables.redis import increment, get_value

def record_page_view(page_slug):
    key = f'views:page:{page_slug}'
    views = increment(key)
    return views

def get_page_views(page_slug):
    key = f'views:page:{page_slug}'
    return get_value(key, default=0)
```

### Cache Invalidation

```python
from reusables.redis import invalidate_pattern

def invalidate_user_cache(user_id):
    # Invalidate all cache for this user
    pattern = f'cache:user:{user_id}:*'
    count = invalidate_pattern(pattern)
    print(f'Invalidated {count} cache entries')

def clear_all_sessions():
    # Clear all sessions
    count = invalidate_pattern('session:*')
    print(f'Cleared {count} sessions')
```

### Structured Data with Hashes

```python
from reusables.redis import hash_set, hash_get, hash_get_all

def update_user_profile(user_id, **fields):
    key = f'user:{user_id}:profile'
    for field, value in fields.items():
        hash_set(key, field, value)

def get_user_profile(user_id):
    key = f'user:{user_id}:profile'
    return hash_get_all(key)

# Usage
update_user_profile('123', name='Noah', age=21, city='Oslo')
profile = get_user_profile('123')
```

---

## Performance Tips

1. **Use bulk operations** when possible (`set_many`, `get_many`)
2. **Set appropriate TTLs** - Don't cache forever
3. **Use hashes** for related data instead of multiple keys
4. **Namespace your keys** to avoid collisions
5. **Limit pattern scans** - Use `find_keys` sparingly
6. **Use counters** for metrics instead of fetching and incrementing

---

## Error Handling

The client handles connection errors gracefully:

```python
from reusables.redis import get_redis_client
import redis

try:
    r = get_redis_client()
    r.ping()
except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")
    # Fallback to database or return cached error
```

---

## Testing

Reset the client singleton between tests:

```python
from reusables.redis import RedisClient

def teardown():
    RedisClient.reset()
```

---

## Connection Details

### Local Development
- **Host:** `34.66.188.104` (external IP)
- **Port:** `6379`
- **Environment:** Set `ENVIRONMENT=local` or leave unset

### Production (Cloud Run)
- **Host:** `10.128.0.3` (internal VPC IP)
- **Port:** `6379`
- **Environment:** Automatically set to `production` by deploy script
- **VPC Connector:** `redis-connector` enables internal access

---

## Contributing

When adding new Redis utilities:

1. Add function to `client.py`
2. Export from `__init__.py`
3. Document in this README
4. Add usage examples

---

## Related Documentation

- [FirstApi README](../../FirstApi/README.md) - See Redis integration in action
- [Redis Infrastructure](../../../iac/redis/README.md) - Redis server setup
- [VPC Connector](../../../iac/networking/README.md) - Network configuration

