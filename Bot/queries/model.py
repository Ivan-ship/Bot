from sqlalchemy import String, MetaData, BigInteger, Boolean, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

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

    subscribe = relationship("Subscribe", back_populates="users", cascade="all, delete-orphan")


class Subscribe(Base):
    __tablename__ = "subscribe"
    sub_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    url: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column(Integer)
    plan: Mapped[str] = mapped_column(String(50))
    id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    users = relationship("User", back_populates="subscribe")