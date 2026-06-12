from pydantic import BaseModel

class User:
    id: int
    is_bot: bool
    first_name: str | None = None
    last_name: str | None = None
    username: str
    language_code: str | None = None
    is_premium: bool | None = None