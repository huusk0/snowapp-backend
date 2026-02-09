from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.rectangle import RectangleIn, RectangleEdges
from ..logic.rectModel import Rectangle, GeometryService

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
