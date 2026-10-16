"""
SpamShield API Testing Examples
Complete test suite with cURL, Python, and JavaScript examples
"""

# ============================================================================
# 1. AUTHENTICATION TESTS
# ============================================================================

# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'

# Response:
# {
#   "id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "is_active": true,
#   "created_at": "2026-06-12T15:46:52.063Z"
# }

# Login user
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'

# Response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "token_type": "bearer"
# }

# Get current user (requires token)
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'

# ============================================================================
# 2. PREDICTION TESTS
# ============================================================================

TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Predict single message
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Click here to claim your FREE prize now!!!",
    "model_name": "ensemble"
  }'

# Response:
# {
#   "id": 1,
#   "message": "Click here to claim your FREE prize now!!!",
#   "is_spam": true,
#   "spam_probability": 0.9485,
#   "model_used": "ensemble",
#   "detected_keywords": ["free", "prize", "click", "claim"],
#   "created_at": "2026-06-12T15:46:52.063Z"
# }

# Predict safe message
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi John, can we meet tomorrow to discuss the project?",
    "model_name": "ensemble"
  }'

# Response:
# {
#   "id": 2,
#   "message": "Hi John, can we meet tomorrow to discuss the project?",
#   "is_spam": false,
#   "spam_probability": 0.0234,
#   "model_used": "ensemble",
#   "detected_keywords": [],
#   "created_at": "2026-06-12T15:46:52.063Z"
# }

# Get prediction history
curl -X GET "http://localhost:8000/api/v1/history?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"

# Response:
# {
#   "total_predictions": 42,
#   "spam_count": 8,
#   "safe_count": 34,
#   "recent_predictions": [
#     {
#       "id": 42,
#       "message": "...",
#       "is_spam": true,
#       "spam_probability": 0.95,
#       ...
#     },
#     ...
#   ]
# }

# Get user metrics
curl -X GET http://localhost:8000/api/v1/metrics \
  -H "Authorization: Bearer $TOKEN"

# Response:
# {
#   "total_predictions": 42,
#   "spam_detected": 8,
#   "accuracy": 0.992,
#   "precision": 0.988,
#   "recall": 0.975,
#   "active_model": "ensemble"
# }

# ============================================================================
# 3. MODEL MANAGEMENT TESTS
# ============================================================================

# List available models
curl -X GET http://localhost:8000/api/v1/models \
  -H "Authorization: Bearer $TOKEN"

# Response:
# {
#   "total_models": 3,
#   "models": [
#     {
#       "id": 1,
#       "name": "multinomial_nb_v1",
#       "version": "1.0",
#       "model_type": "naive_bayes",
#       "accuracy": 0.98,
#       "precision": 0.97,
#       "recall": 0.96,
#       "is_active": false
#     },
#     {
#       "id": 2,
#       "name": "bert_v1",
#       "version": "1.0",
#       "model_type": "bert",
#       "accuracy": 0.992,
#       "precision": 0.988,
#       "recall": 0.975,
#       "is_active": true
#     }
#   ]
# }

# ============================================================================
# 4. ADMIN TESTS (requires admin token)
# ============================================================================

# Trigger model retraining
curl -X POST http://localhost:8000/api/v1/admin/train \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Response:
# {
#   "message": "Training job queued",
#   "status": "pending",
#   "job_id": "job_123",
#   "estimated_time": "5 minutes"
# }

# Get admin dashboard
curl -X GET http://localhost:8000/api/v1/admin/dashboard \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Response:
# {
#   "total_users": 157,
#   "total_predictions": 12453,
#   "spam_detected": 2103,
#   "spam_percentage": 16.89,
#   "active_models": 1
# }

# ============================================================================
# 5. PYTHON CLIENT EXAMPLES
# ============================================================================

"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123"
})
print(response.json())

# Login
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "alice@example.com",
    "password": "SecurePass123"
})
token = login_response.json()["access_token"]

# Predict
headers = {"Authorization": f"Bearer {token}"}
predict_response = requests.post(f"{BASE_URL}/predict", 
    headers=headers,
    json={"message": "You won a FREE iPhone 13!"}
)
print(predict_response.json())

# Get history
history_response = requests.get(f"{BASE_URL}/history", headers=headers)
print(f"Total predictions: {history_response.json()['total_predictions']}")

# Get metrics
metrics_response = requests.get(f"{BASE_URL}/metrics", headers=headers)
print(f"Accuracy: {metrics_response.json()['accuracy']:.2%}")
"""

# ============================================================================
# 6. JAVASCRIPT CLIENT EXAMPLES
# ============================================================================

"""
// Fetch API Example
const BASE_URL = "http://localhost:8000/api/v1";

// Register
async function register() {
    const response = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: 'bob',
            email: 'bob@example.com',
            password: 'SecurePass123'
        })
    });
    return await response.json();
}

// Login
async function login() {
    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: 'bob@example.com',
            password: 'SecurePass123'
        })
    });
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data.access_token;
}

// Predict
async function predictSpam(message) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${BASE_URL}/predict`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            model_name: 'ensemble'
        })
    });
    return await response.json();
}

// Get metrics
async function getMetrics() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${BASE_URL}/metrics`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return await response.json();
}

// Usage
(async () => {
    await register();
    await login();
    
    const prediction = await predictSpam('Claim your FREE prize now!');
    console.log(prediction);
    
    const metrics = await getMetrics();
    console.log(`Accuracy: ${(metrics.accuracy * 100).toFixed(2)}%`);
})();
"""

# ============================================================================
# 7. POSTMAN COLLECTION STRUCTURE
# ============================================================================

"""
SpamShield API Collection
├── Authentication
│   ├── Register
│   ├── Login
│   ├── Refresh Token
│   └── Get Me
├── Predictions
│   ├── Predict Spam
│   ├── Get History
│   └── Get Metrics
├── Models
│   └── List Models
└── Admin
    ├── Trigger Training
    └── Get Dashboard

Import this into Postman:
https://github.com/yourusername/spamshield/postman-collection.json
"""
