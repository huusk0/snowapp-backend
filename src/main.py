from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.rectangle import RectangleIn, RectangleEdges, SnowSectorOut, Point
from .logic.rectModel import Rectangle, GeometryService

app = FastAPI()
solver = GeometryService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/greeting/")
def get_item():
    return {"text": "Hello world from API"}


@app.post("/api/rectangles/", response_model=list[RectangleEdges])
def modify_rects(rectangles: list[RectangleIn]) -> list[RectangleEdges]:
    rectangle_edges = []
    for rect in rectangles:
        r = Rectangle(**rect.model_dump())
        edges = solver.calculate_edge_points(r)
        rectangle_edges.append(edges)
    return rectangle_edges


@app.post("/api/snowsectors/", response_model=list[SnowSectorOut])
def calculate_snowsectors(rectangles: list[RectangleIn]) -> list[SnowSectorOut]:
    rectangles_list = []
    for rect in rectangles:
        r = Rectangle(**rect.model_dump())
        rectangles_list.append(r)
    snow_sectors = solver.split_to_sectors(rectangles_list)
    return [
        SnowSectorOut(
            coords=Point(x=s.coords[0], y=s.coords[1]),
            snow_load=s.snow_load,
            color=s.color,
            dump_site=s.dump_site,
        )
        for s in snow_sectors
    ]


# @app.post("/api/snowsectors/")
# def calculate_snowsectors(rectangles: list[RectangleIn]):
#     rectangles_list = []
#     for rect in rectangles:
#         r = Rectangle(**rect.model_dump())
#         rectangles_list.append(r)
#     snow_sectors = solver.split_to_sectors(rectangles_list)
#     return snow_sectors
