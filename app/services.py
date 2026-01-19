from sqlalchemy.orm import Session
from . import client, crud, schemas, database
import logging

logger = logging.getLogger(__name__)

from datetime import datetime, timedelta

def sync_teeinblue_orders_service(start_days_ago=1, end_days_ago=0):
    """
    Bot 1: Fetch orders from Teeinblue.
    Args:
        start_days_ago (int): Start filtering from X days ago.
        end_days_ago (int): End filtering at Y days ago. (0 = now)
    """
    db = database.SessionLocal()
    page = 1
    limit_per_page = 25
    max_pages_safety = 50 
    
    # Calculate Date Range (Aligned to Start of Day)
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # start_days_ago=1 => Today (today_start - 0 days)
    start_date = today_start - timedelta(days=start_days_ago - 1)
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    end_date_str = None
    if end_days_ago > 0:
        # end_days_ago > 0 => End of that specific filtering day (23:59:59)
        # e.g. end_days_ago=1 => End of Today (future?) No wait. 
        # If I want 'Yesterday' (1 day ago), end_days_ago=1.
        # Logic: today_start - (1-1) = today_start. 
        # Wait, if I user input 1 to 1 (Just today). Start = Today 00:00. End = Today 23:59.
        # If user input 7 to 2. Start = Day 7 ago (00:00). End = Day 2 ago (23:59).
        
        target_end_day = today_start - timedelta(days=end_days_ago - 1)
        end_date = target_end_day.replace(hour=23, minute=59, second=59)
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    range_msg = f"Last {start_days_ago} days" if end_days_ago == 0 else f"{start_days_ago} days ago to {end_days_ago} days ago"

    try:
        logger.info(f"[Bot 1 Sync] Starting range: {range_msg}...")
        c = client.TeeinblueClient()
        
        while page <= max_pages_safety:
            logger.info(f"[Bot 1 Sync] Fetching page {page}...")
            
            # 1. Fetch Page with Date Range
            data = c.get_ready_orders(
                page=page, 
                limit=limit_per_page, 
                start_date=start_date_str,
                end_date=end_date_str
            )
            
            if not data:
                logger.info("[Bot 1] No data returned from API. Stopping.")
                break

            orders_list = data.get('data', [])
            if not orders_list:
                logger.info(f"[Bot 1] Page {page} is empty. Sync finished.")
                break
            
            count = 0
            for item in orders_list:
                order_id = str(item.get('id'))
                
                # 2. Get Detail
                details = c.get_order_detail(order_id)
                if not details:
                    continue
                    
                # 3. Map Data
                order_schema = schemas.OrderCreate(
                    id=str(details.get('id')),
                    ref_id=details.get('name') or details.get('ref_id'),
                    status=str(details.get('status')),
                    customer_info=details.get('customer'),
                    line_items=details.get('line_items'),
                    full_data=details 
                )
                
                # 4. Save to DB
                crud.upsert_order(db, order_schema)
                count += 1
            
            logger.info(f"[Bot 1] Page {page} done. Processed {count} orders.")
            
            # Check pagination meta to decide if we should stop
            meta = data.get('meta', {})
            current_page = meta.get('current_page')
            last_page = meta.get('last_page')
            
            # If API doesn't return standard meta, use list length fallback
            if len(orders_list) < limit_per_page:
                break
                
            if last_page and current_page >= last_page:
                break
                
            page += 1
            
    except Exception as e:
        logger.error(f"[Bot 1] Error during sync: {e}")
    finally:
        db.close()

def send_orders_to_manufacturer_service():
    """
    Bot 2: Poll local DB for orders that havent been sent to manufacturer.
    (Placeholder for now)
    """
    logger.info("[Bot 2] Checking for orders to send to Manufacturer...")
    # Logic to query DB for 'pending_manufacturer' status would go here
    pass
