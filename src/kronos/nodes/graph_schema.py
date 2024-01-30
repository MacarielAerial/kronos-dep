from enum import Enum
from typing import TypedDict


class NodeAttrKey(str, Enum):
    ntype = "ntype"
    raw_text = "raw_text"
    ner = "ner"
    nid_parent = "nid_parent"


class EdgeAttrKey(str, Enum):
    etype = "etype"
    direction = "direction"
    distance = "distance"


class NodeType(str, Enum):
   event = "EVENT"
   duration = "DURATION"
   month_day = "MONTH_DAY"
   year = "YEAR"
   month = "MONTH"
   day = "DAY"
   day_of_week = "DAY_OF_WEEK"
   loc = "LOC"
   person = "PERSON"
   time = "TIME"
   other = "OTHER"


class EdgeType(str, Enum):
    layout = "Layout"
