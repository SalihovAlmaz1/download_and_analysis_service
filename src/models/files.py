from datetime import datetime

from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import Base


class File(Base):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    downloaded_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
