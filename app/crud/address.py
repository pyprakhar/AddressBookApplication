from sqlalchemy.orm import Session
from app.model import models, schema
from app.utils import nearby_address

def create_address(db: Session, address: schema.AddressCreate) -> models.Address:
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session):
    return db.query(models.Address).all()

def get_nearby_addresses(db: Session, latitude: float, longitude: float, distance_km: float):
    addresses = db.query(models.Address).all()
    nearby = []
    for addr in addresses:
        dist = nearby_address.haversine(latitude, longitude, addr.latitude, addr.longitude)
        if dist <= distance_km:
            nearby.append(addr)
    return nearby

def update_address(db: Session, address_id: str, address: schema.AddressUpdate):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        return None
    for field, value in address.dict(exclude_unset=True).items():
        setattr(db_address, field, value)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: str):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        return None
    db.delete(db_address)
    db.commit()
    return db_address
