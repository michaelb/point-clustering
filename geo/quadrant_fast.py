"""
quadrants are rectangular boxes delimiting a set of items.
they are used in display to compute image sizes.
"""

class Quadrant:
    """
    enclosing rectangles.
    """
    def __init__(self, min_coordinates, max_coordinates):
        self.min_coordinates = list(min_coordinates)
        self.max_coordinates = list(max_coordinates)
        self.childs = []
        self.parent = None
        self.list_point_inside = []
        self.count = 0
        self.extended = None


    def copy(self, distance):
        """
        return deepcopy of given quadrant.
        """
        return Quadrant(
            list(self.min_coordinates), list(self.max_coordinates), distance)


    def extend(self ,distance):
        """
        return deepcopy of given quadrant.
        """
        self.extended =  Quadrant(
            list([x-distance for x in self.min_coordinates]), list([x + distance for x in self.max_coordinates]))

    @classmethod
    def empty_quadrant(cls, dimension):
        """
        return an empty quadrant in space of given dimension
        """
        min_coordinates = []
        max_coordinates = []
        for _ in range(dimension):
            min_coordinates.append(float('+inf'))
            max_coordinates.append(float('-inf'))
        return cls(min_coordinates, max_coordinates)

    def taille(self,arg='min'):#size of the thinnest side of quadrant
        if arg == 'min':
            return min([cmax - cmin for cmax, cmin in zip(self.max_coordinates, self.min_coordinates)])
        elif arg == 'max':
            return max([cmax - cmin for cmax, cmin in zip(self.max_coordinates, self.min_coordinates)])


    def contain(self, point, margin = 0):
        for i, point_coordinate in enumerate(point.coordinates):
            if not (self.min_coordinates[i] - margin <= point_coordinate <= self.max_coordinates[i] + margin):
                return 0
        return 1
    def add_point(self, added_point):
        """
        register a point inside the quadrant.
        update limits if needed.
        """
        for i, added_coordinate in enumerate(added_point.coordinates):
            if added_coordinate < self.min_coordinates[i]:
                self.min_coordinates[i] = added_coordinate
            if added_coordinate > self.max_coordinates[i]:
                self.max_coordinates[i] = added_coordinate

    def update(self, other):
        """
        expands self quadrant by taking constraints from other quadrant into account.
        the new one will have the minimal size needed to contain both initial ones.
        """
        assert len(self.min_coordinates) == len(other.min_coordinates), \
            'merge in different spaces'
        for i, coordinate in enumerate(other.min_coordinates):
            if self.min_coordinates[i] > coordinate:
                self.min_coordinates[i] = coordinate
        for i, coordinate in enumerate(other.max_coordinates):
            if self.max_coordinates[i] < coordinate:
                self.max_coordinates[i] = coordinate

    def limits(self, index):
        """
        returns array of limits for a given coordinate index
        """
        return (self.min_coordinates[index], self.max_coordinates[index])

    def inflate(self, distance):
        """
        get bigger quadrant containing original one + any point outside
        original at distance less than given
        """
        self.min_coordinates = [c - distance for c in self.min_coordinates]
        self.max_coordinates = [c + distance for c in self.max_coordinates]

    def minimal_bounding(self,dimension=2):
        """transform self into the smallest quadrant possible that still
        contains the points of the previous one"""
        if not self.list_point_inside:
            self.min_coordinates = [0] * dimension
            self.max_coordinates = [0] * dimension
        else:
            new_max_coordinates = [max([p.coordinates[i] for p in self.list_point_inside]) for i in range(dimension)]
            new_min_coordinates = [min([p.coordinates[i] for p in self.list_point_inside]) for i in range(dimension)]

            self.min_coordinates = new_min_coordinates
            self.max_coordinates = new_max_coordinates
    def __eq__(self, other):
        return self.min_coordinates,self.max_coordinates == other.min_coordinates, other.max_coordinates
    def get_arrays(self):
        """
        returns arrays of limits
        """
        return (self.min_coordinates, self.max_coordinates)
