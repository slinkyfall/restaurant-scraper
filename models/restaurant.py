from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Restaurant:
    """Modelo de datos para restaurante"""
    name: str
    address: str
    postal_code: str
    phone: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    cuisine_type: Optional[str] = None
    business_hours: Optional[Dict[str, str]] = None
    website: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    scraped_at: datetime = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario"""
        return {
            'name': self.name,
            'address': self.address,
            'postal_code': self.postal_code,
            'phone': self.phone,
            'rating': self.rating,
            'review_count': self.review_count,
            'cuisine_type': self.cuisine_type,
            'business_hours': self.business_hours,
            'website': self.website,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'scraped_at': self.scraped_at
        }