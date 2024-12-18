from pydantic import BaseModel, Field
from typing import List, Optional, Any

# Base model for books
class BookBase(BaseModel):
    id: str
    title: str
    authors: List[str]
    description: str
    category: List[str]
    publisher: str
    publish_date: str
    price: float
    quantity_available: int
    location: Any

# Create book model (no ID yet)
class BookCreate(BaseModel):
    title: str
    authors: List[str]
    description: str
    category: List[str]
    publisher: str
    publish_date: str
    price: float
    quantity_available: int
    location: Any

# Update book model (optional fields)
class BookUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    description: Optional[str] = None
    category: Optional[List[str]] = None
    publisher: Optional[str] = None
    publish_date: Optional[str] = None
    price: Optional[float] = None
    quantity_available: Optional[int] = None
    location: Any = None

# Full book response model (includes ID)
class Book(BookBase):
    pass
