from typing import List, Union

from pydantic import BaseModel


class Coord(BaseModel):
    x: int
    y: float


class Pnl(BaseModel):
    pnl: List[Union[Coord, None]]
    pnl_percent: List[Union[Coord, None]]
    index_pnl: List[Union[Coord, None]]
    date_from: str
    date_to: str
