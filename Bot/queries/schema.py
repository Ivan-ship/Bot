from pydantic import BaseModel
from datetime import date

class User:
    id: int
    is_bot: bool
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    is_admin: bool | None = None
    created_at: date


class Subscribe:
    sub_id : int
    start_date: date
    end_date: date
    url: str
    id: int
    price: int
    plan: str