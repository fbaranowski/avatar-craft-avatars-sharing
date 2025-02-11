from pydantic import BaseModel


class AvatarShare(BaseModel):
    from_user: str
    to_user: str
    avatar_id: int
