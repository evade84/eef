from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    index: int
    signature: Optional[str]
    text: str


class Pool(BaseModel):
    address: str
    tag: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[str] = None
    write_key_required: bool
    read_key_required: bool
    indexable: bool


class Messages(BaseModel):
    total: int
    messages: list[Message]


class Pools(BaseModel):
    total: int
    pools: list[Pool]


class Node(BaseModel):
    name: str
    version: str
