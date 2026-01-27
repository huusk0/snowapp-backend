class SnowSector:
    def __init__(self, coords=None, snow_load=None, color="yellow", dump=False):
        self.coords = coords
        self.snow_load = snow_load
        self.color = color
        self.dump = dump

    def __repr__(self):
        return f"Snow sector at: {self.coords}"
