from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from app.database.db import Base
from uuid import uuid4

# Define the Address model representing the addresses table in the database
class Address(Base):
    __tablename__ = "addresses"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # Database-level unique constraint to prevent duplicate name + coordinates
    __table_args__ = (
        UniqueConstraint('name', 'latitude', 'longitude', name='uq_address_name_lat_lon'),
    )
