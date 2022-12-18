from pydantic import BaseModel, Extra
from typing import Dict, List, Sequence, Set, Tuple


class Config(BaseModel, extra=Extra.ignore):
    sum666_datapath: str = "data/sum666/data.json"
    sum666_group: Set[str] = {}
    sum666_user: Set[str] = {}
    sum666_output: Set[str] = {
        "您又在扣6了, {0}大爷您歇会吧",
        "您总共扣了{2}次6了, 您不累我都累了",
        "您在{3}又扣了一次6, 历史不会记住您, 但我会"
    }
    sum666_keyword: Set[str] = {"666", "6", "liu", "六", "six"}
