class Place:
    def __init__(self, name, i):
        self.name = name
        self.index = int(i)
        self.paths = None
        self.dist = None

    def get_index(self):
        return self.index

    def get_name(self):
        return self.name

    def set_distances(self, g):
        self.dist = g[self.index][:]

    def set_paths(self, paths):
        self.paths = paths[self.index][:]

    def get_distance(self, j):
        return self.dist[j]

    def get_path(self, j):
        return self.paths[j]

    def __str__(self):
        tup = (self.index, self.name, self.dist, self.paths)
        return "Node {}, {}: distances {}, paths {}".format(*tup)

    def __repr__(self):
        tup = (self.index, self.name, self.dist, self.paths)
        return str(tup)
