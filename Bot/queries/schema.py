from pydantic import BaseModel
from datetime import date

class User:
    id: int
    is_bot: bool
    first_name: str | None = None
    last_name: str | None = None
    username: str
    language_code: str | None = None
    is_premium: bool | None = None


class Subscribe:
    sub_id : int
    start_date: date
    end_date: date
    url: str
    id: int
    price: int