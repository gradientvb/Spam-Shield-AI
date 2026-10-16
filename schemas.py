from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============= AUTH SCHEMAS =============
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============= PREDICTION SCHEMAS =============
class PredictionRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    model_name: Optional[str] = None

class PredictionResponse(BaseModel):
    id: int
    message: str
    is_spam: bool
    spam_probability: float
    model_used: str
    detected_keywords: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionHistory(BaseModel):
    total_predictions: int
    spam_count: int
    safe_count: int
    recent_predictions: List[PredictionResponse]

# ============= MODEL SCHEMAS =============
class SpamModelResponse(BaseModel):
    id: int
    name: str
    version: str
    model_type: str
    accuracy: float
    precision: float
    recall: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MetricsResponse(BaseModel):
    total_predictions: int
    spam_detected: int
    accuracy: float
    precision: float
    recall: float
    active_model: str

# ============= ERROR SCHEMAS =============
class ErrorResponse(BaseModel):
    detail: str
    status_code: int
