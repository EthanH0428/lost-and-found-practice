from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.item import ItemCategory, ItemStatus


class ItemCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120, examples=["검은색 무선 이어폰 케이스"])
    description: str = Field(min_length=5, max_length=2000)
    category: ItemCategory
    found_location: str = Field(min_length=2, max_length=150, examples=["중앙도서관 2층"])
    found_at: datetime
    reporter_name: str = Field(min_length=2, max_length=80)
    reporter_contact: str = Field(min_length=3, max_length=120)
    photo_url: str | None = Field(default=None, max_length=2048)


class ItemStatusUpdate(BaseModel):
    status: ItemStatus


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: ItemCategory
    found_location: str
    found_at: datetime
    reporter_name: str
    reporter_contact: str
    photo_url: str | None
    status: ItemStatus
    claimed_at: datetime | None
    created_at: datetime
    updated_at: datetime
