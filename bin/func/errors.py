class Curve_to_short(Exception):
    "Raised when wire length is less than the minimum stted for the selected tool."
    pass


class Unfound_edge(Exception):
    "Raised when distance on wire do not correspond to a edge"
    pass


class Point_creation_error(Exception):
    "Failed to create point"
    pass


class Orthogonality_error(Exception):
    "The vectors are not orthogonal to each other"
    pass
