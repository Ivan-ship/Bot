from sqlalchemy import String, MetaData, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

metadata_obj = MetaData()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    is_bot: Mapped[bool] = mapped_column(Boolean)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(100))
    language_code: Mapped[str| None] = mapped_column(String(100), nullable=True)
    is_premium: Mapped[bool | None] = mapped_column(Boolean, nullable=True)