from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_order(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def upsert_order(db: Session, order_data: schemas.OrderCreate):
    db_order = get_order(db, order_data.id)
    if db_order:
        # Update existing
        db_order.ref_id = order_data.ref_id
        db_order.status = order_data.status
        db_order.customer_info = order_data.customer_info
        db_order.line_items = order_data.line_items
        db_order.full_data = order_data.full_data
        db_order.synced_at = datetime.now()
    else:
        # Create new
        db_order = models.Order(
            id=order_data.id,
            ref_id=order_data.ref_id,
            status=order_data.status,
            customer_info=order_data.customer_info,
            line_items=order_data.line_items,
            full_data=order_data.full_data
        )
        db.add(db_order)
    
    try:
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        print(f"Error upserting: {e}")
        return None
        
    return db_order
