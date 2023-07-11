
def simplify_coords(coords):
    if isinstance(coords, (list, tuple)):
        return [simplify_coords(coord) for coord in coords]
    elif isinstance(coords, float):
        return round(coords, 7)
    raise Exception("Param is {}. Should be <list>, <tuple> or <float>".format(type(coords)))
