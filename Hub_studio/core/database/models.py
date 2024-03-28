from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    date_created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())#func.now() - подтягивает текущее время
    date_updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Assue(Base):
    __tablename__ = "assue"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    decision: Mapped[Optional[str]] = mapped_column(Text)