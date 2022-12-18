from pydantic import BaseModel, Extra
from typing import Set


class Config(BaseModel, extra=Extra.ignore):
    open_group: Set[str] = {}
    open_user: Set[str] = {}
    msg_group: str = {}
    target_group: Set[str] = {}
    default_keyword: Set[str] = {}
