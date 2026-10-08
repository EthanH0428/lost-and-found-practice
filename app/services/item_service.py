from datetime import datetime, timezone

from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session

from app.models.item import Item, ItemCategory, ItemStatus
from app.schemas.item import ItemCreate


def create_item(db: Session, payload: ItemCreate) -> Item:
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)


def list_items(
    db: Session,
    status_filter: ItemStatus | None,
    category: ItemCategory | None,
    keyword: str | None,
    offset: int,
    limit: int,
) -> list[Item]:
    statement: Select[tuple[Item]] = select(Item)

    if status_filter is not None:
        statement = statement.where(Item.status == status_filter)
    if category is not None:
        statement = statement.where(Item.category == category)
    if keyword is not None:
        search = f"%{keyword.strip()}%"
        statement = statement.where(or_(Item.title.ilike(search), Item.description.ilike(search)))

    statement = statement.order_by(Item.found_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement))


def update_item_status(db: Session, item: Item, new_status: ItemStatus) -> Item:
    item.status = new_status
    if new_status == ItemStatus.CLAIMED and item.claimed_at is None:
        item.claimed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item
