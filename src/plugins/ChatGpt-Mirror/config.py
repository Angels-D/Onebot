from pydantic import BaseModel, Extra
from typing import Set


class Config(BaseModel, extra=Extra.ignore):
    chatgpt_cd_time: int = 60
    chatgpt_openid: Set[str] = {}
    chatgpt_group: Set[str] = {}
