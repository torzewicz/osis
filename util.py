class SelfLoopException(Exception):

    def __init__(self, node):
        self.node = node
        self.message = f"Pętla na wierzchołku {node}"
        super().__init__(self.message)


def load_graph(path):
    with open(path) as fp:
        from_edges = []
        to_edges = []
        weights_list = []
        defined_k = None
        beginning = None
        end = None

        number_of_nodes = int(fp.readline().strip())

        line = fp.readline()
        while line and line != "\n":
            edge_list = (line.strip().split(" "))
            edge_start = int(edge_list[0])
            edge_end = int(edge_list[1])
            if edge_start == edge_end:
                raise SelfLoopException(edge_start)
            from_edges.append(edge_start)
            to_edges.append(edge_end)
            weights_list.append(int(edge_list[2]))
            line = fp.readline()

        line = fp.readline()

        while line and line != "\n":
            defined_k = int(line)
            line = fp.readline()

        line = fp.readline()
        while line and line != "\n":
            where = line.strip().split(" ")
            beginning = int(where[0])
            end = int(where[1])
            line = fp.readline()

    return number_of_nodes, from_edges, to_edges, weights_list, defined_k, beginning, end
