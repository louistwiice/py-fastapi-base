from typing import List, Union, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: str
    owner_id: str



    class Config:
        orm_mode = True
