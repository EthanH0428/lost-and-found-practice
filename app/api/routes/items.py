from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.item import ItemCategory, ItemStatus
from app.schemas.item import ItemCreate, ItemRead, ItemStatusUpdate
from app.services.item_service import create_item, get_item, list_items, update_item_status

router = APIRouter()


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def register_item(payload: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    """Register a found item reported on campus."""
    return create_item(db, payload)


@router.get("", response_model=list[ItemRead])
def read_items(
    status_filter: ItemStatus | None = Query(default=None, alias="status"),
    category: ItemCategory | None = None,
    keyword: str | None = Query(default=None, min_length=1, max_length=100),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[ItemRead]:
    """Browse found items with optional filters."""
    return list_items(db, status_filter, category, keyword, offset, limit)


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.patch("/{item_id}/status", response_model=ItemRead)
def change_item_status(
    item_id: int,
    payload: ItemStatusUpdate,
    db: Session = Depends(get_db),
) -> ItemRead:
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return update_item_status(db, item, payload.status)
