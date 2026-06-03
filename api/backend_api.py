from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

app = FastAPI(title="Portable Preferences Portal API")

# --- Memory Storage Emulation ---
DATABASE = {}

# --- Pydantic Schema Declarations (Auto-validating Data Models) ---
class MetaModel(BaseModel):
    version: str
    updated_at: datetime
    profile_name: str

class PrivacyModel(BaseModel):
    data_sharing: bool
    ad_personalization: bool
    visibility: Literal["public", "contacts_only", "private"]

class DisplayModel(BaseModel):
    theme: Literal["light", "dark", "system"]
    font_size_scale: float = Field(ge=0.5, le=2.0)

class LightingModel(BaseModel):
    default_brightness: int = Field(ge=0, le=100)
    color_temperature_kelvin: int = Field(ge=2000, le=6500)
    adaptive_lighting: bool

class ClimateModel(BaseModel):
    preferred_unit: Literal["C", "F"]
    target_temperature_home: float
    target_temperature_away: float

class SmartHomeModel(BaseModel):
    climate: ClimateModel
    lighting: LightingModel

class UniversalProfile(BaseModel):
    meta: MetaModel
    privacy_and_communication: PrivacyModel
    display: DisplayModel
    smart_home: SmartHomeModel

# --- API Endpoints ---
@app.put("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def update_profile(user_id: str, profile: UniversalProfile):
    """Saves and validates an incoming user profile setting payload."""
    DATABASE[user_id] = profile.dict()
    return {"status": "success", "message": f"Preferences updated for user {user_id}."}

@app.get("/profile/{user_id}", response_model=UniversalProfile)
async def get_profile(user_id: str):
    """Retrieves the unified portal configuration for a specific device sync request."""
    if user_id not in DATABASE:
        raise HTTPException(status_code=404, detail="User profile configuration not found.")
    return DATABASE[user_id]
