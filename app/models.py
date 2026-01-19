from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.sql import func
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True) # Teeinblue ID
    ref_id = Column(String, index=True) # Order Number (e.g. #1234)
    status = Column(String) # Processing status
    
    # Storing complex objects as JSON
    customer_info = Column(JSON, nullable=True)
    line_items = Column(JSON, nullable=True)
    
    full_data = Column(JSON, nullable=True) # Full JSON from Teeinblue
    
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
