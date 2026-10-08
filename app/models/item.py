from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ItemCategory(str, Enum):
    ELECTRONICS = "electronics"
    WALLET = "wallet"
    ID_CARD = "id_card"
    CLOTHING = "clothing"
    BOOK = "book"
    ETC = "etc"


class ItemStatus(str, Enum):
    RECEIVED = "received"
    STORED = "stored"
    CLAIMED = "claimed"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[ItemCategory] = mapped_column(SqlEnum(ItemCategory), index=True)
    found_location: Mapped[str] = mapped_column(String(150))
    found_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    reporter_name: Mapped[str] = mapped_column(String(80))
    reporter_contact: Mapped[str] = mapped_column(String(120))
    photo_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    status: Mapped[ItemStatus] = mapped_column(
        SqlEnum(ItemStatus), default=ItemStatus.RECEIVED, index=True
    )
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
