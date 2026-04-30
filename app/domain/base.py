from datetime import datetime
import uuid
import inflect
from sqlalchemy import func, TIMESTAMP, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

p = inflect.engine()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # Используем server_default для UUID, чтобы БД сама генерила ID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v7()
    )

    is_active: Mapped[bool] = mapped_column(server_default=func.true())

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),  # Всегда используй таймзоны!
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return p.plural(cls.__name__.lower())
