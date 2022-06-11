from pydantic import BaseModel


class Message(BaseModel):
    index: int
    signature: str | None
    text: str


class Pool(BaseModel):
    address: str
    tag: str | None = None
    description: str | None = None
    creator: str | None = None
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
