'''
Requirement:

Create an address book application where API users can create, update and delete
addresses.
The address should:
- contain the coordinates of the address.
- be saved to an SQLite database.
- be validated
API Users should also be able to retrieve the addresses that are within a given distance and
location coordinates.
'''

from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from app.model import models, schema
from app.utils import nearby_address
from app.database.db import get_db
from sqlalchemy.orm import Session
import logging
from app.crud import address as crud_address

# Set up logging and reuse the same logger as the main application
logger = logging.getLogger("uvicorn.error")

# Api router for address related endpoints
address_router = APIRouter( tags=["Addresses"])

#--------------------------------- Address API Endpoints ------------------------------------#

#--------------------------------
# Create the address
#--------------------------------
@address_router.post(
    "/addresses/",
    response_model=schema.AddressOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="Create a new address with name, street, city, state, country, latitude, and longitude."
)
def create_address(address: schema.AddressCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating address: {address.name}")
    try:
        # Check for duplicates
        existing = db.query(models.Address).filter(
            models.Address.name == address.name,
            models.Address.latitude == address.latitude,
            models.Address.longitude == address.longitude
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address with same name and coordinates already exists"
            )

        # Create address
        return crud_address.create_address(db, address)
    except Exception as exc:
        logger.exception("Failed to create address")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


#--------------------------------    
# Get all address 
#--------------------------------
@address_router.get(
    "/addresses/",
    response_model=list[schema.AddressOut],
    summary="Get all addresses",
    description="Retrieve all addresses stored in the database."
)
def get_addresses(db: Session = Depends(get_db)):
    try:
        return crud_address.get_addresses(db)
    except Exception as exc:
        logger.exception("Failed to fetch addresses")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


#--------------------------------
# Get nearby addresses
#--------------------------------

@address_router.get(
    "/addresses/nearby",
    response_model=list[schema.AddressOut],
    summary="Get nearby addresses",
    description="Retrieve addresses within a specified distance (in km) from given latitude and longitude."
)
def get_nearby_addresses(latitude: float, longitude: float, distance_km: float, db: Session = Depends(get_db)):
    try:
        return crud_address.get_nearby_addresses(db, latitude, longitude, distance_km)
    except Exception as exc:
        logger.exception("Failed to fetch nearby addresses")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

#--------------------------------
# update the address by id
#--------------------------------
@address_router.put(
    "/addresses/{address_id}",
    response_model=schema.AddressOut,
    summary="Update an address",
    description="Update an existing address by its ID. Only fields provided will be updated."
)
def update_address(address_id: str, address: schema.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud_address.update_address(db, address_id, address)
    if not db_address:
        logger.warning(f"Address {address_id} not found for update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return db_address


#--------------------------------    
# delete the address by id
#--------------------------------
@address_router.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an address",
    description="Delete an address by its ID."
)
def delete_address(address_id: str, db: Session = Depends(get_db)):
    db_address = crud_address.delete_address(db, address_id)
    if not db_address:
        logger.warning(f"Address {address_id} not found for deletion")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")