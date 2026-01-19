from sqlalchemy import Column, String, DateTime, JSON, Integer, Float
from sqlalchemy.sql import func
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    # 1. Basic Identity
    id = Column(String, primary_key=True, index=True) # Teeinblue ID
    order_name = Column(String, nullable=True) # e.g. #1003
    ref_id = Column(String, index=True) # External Ref ID
    
    # 2. Status & Values
    status = Column(String) # Teeinblue Processing Status
    financial_status = Column(String, nullable=True) # e.g. paid
    total_price = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    
    # 3. Source Info
    platform_domain = Column(String, nullable=True)
    
    # 4. JSON Data (Complex Structures) at the end
    customer_info = Column(JSON, nullable=True)
    address = Column(JSON, nullable=True)
    line_items = Column(JSON, nullable=True)
    full_data = Column(JSON, nullable=True) # Raw full JSON
    
    # 5. Timestamps
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
