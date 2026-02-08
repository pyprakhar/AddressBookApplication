from pydantic import BaseModel, Field

# Pydantic model for creating a new address with validation for latitude and longitude
class AddressCreate(BaseModel):
    name: str =Field(..., min_length=1, max_length=255)
    street: str
    city: str
    state: str
    country: str
    latitude: float= Field(..., ge=-90, le=90)
    longitude: float= Field(..., ge=-180, le=180)

class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class AddressOut(BaseModel):
    id: str
    name: str
    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
