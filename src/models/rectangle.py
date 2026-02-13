from pydantic import BaseModel, Field


class Point(BaseModel):
    x: int
    y: int


class RectangleIn(BaseModel):
    x: int
    y: int
    width: int = Field(gt=0)
    height: int = Field(gt=0)


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
