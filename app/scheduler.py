from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from . import services
from .config import settings

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler():
    # Bot 1a: Quick Sync (Every 1 min) -> Range: [1 day ago -> NOW]
    scheduler.add_job(
        services.sync_teeinblue_orders_service,
        trigger=IntervalTrigger(minutes=settings.SYNC_INTERVAL_QUICK_MINUTES),
        args=[1, 0], 
        id='teeinblue_quick_sync',
        name='Quick Sync (Last 24h)',
        replace_existing=True
    )

    # Bot 1b: Deep Sync (Every 60 mins) -> Range: [7 days ago -> 1 day ago]
    # Tránh trùng lặp với Quick Sync
    scheduler.add_job(
        services.sync_teeinblue_orders_service,
        trigger=IntervalTrigger(minutes=settings.SYNC_INTERVAL_DEEP_MINUTES),
        args=[7, 1],
        id='teeinblue_deep_sync',
        name='Deep Sync (Days 2-7)',
        replace_existing=True
    )

    # Bot 2: Send DB -> Manufacturer every 1 minutes (Example)
    scheduler.add_job(
        services.send_orders_to_manufacturer_service,
        trigger=IntervalTrigger(minutes=1),
        id='manufacturer_push',
        name='Push orders to Manufacturer',
        replace_existing=True
    )

    scheduler.start()
    logger.info("APScheduler started with tasks.")

def shutdown_scheduler():
    scheduler.shutdown()
