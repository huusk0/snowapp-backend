class Area:
    def __init__(self, height=None, width=None, snow_depth=None, coords=None):
        if height is None or width is None or snow_depth is None or coords is None:
            raise ValueError("fields missing")
        self.height = height
        self.width = width
        self.snow_depth = snow_depth
        self.coords = coords
