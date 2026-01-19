import requests
import logging
from .config import settings

logger = logging.getLogger(__name__)

class TeeinblueClient:
    def __init__(self):
        self.api_key = settings.TEEINBLUE_API_KEY
        self.base_url = settings.TEEINBLUE_API_URL.rstrip('/')
        self.headers = {
            "X-Api-Key": self.api_key,
            "Authorization": f"Bearer {self.api_key}", # As per doc
            "Content-Type": "application/json"
        }
    
    def get_ready_orders(self, page=1, limit=25, start_date=None, end_date=None):
        url = f"{self.base_url}/orders"
        params = {"page": page, "limit": limit}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return None

    def get_order_detail(self, order_id):
        url = f"{self.base_url}/orders/{order_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting order detail {order_id}: {e}")
            return None
