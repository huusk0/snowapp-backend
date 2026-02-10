from pydantic import BaseModel


class Point(BaseModel):
    x: int
    y: int


class RectangleIn(BaseModel):
    x: int
    y: int
    width: int
    height: int


class RectangleEdges(BaseModel):
    topleft: Point
    topright: Point
    bottomleft: Point
    bottomright: Point


class SnowSectorOut(BaseModel):
    coords: Point
    snow_load: int
    color: str
    dump_site: bool
