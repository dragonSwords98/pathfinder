# PathFinder.py
#
# Bryan Ling, courtesy of Receptiviti
#
# 2019-05-01

# README.md
# Requirements
# - install python 3.7.3 or greater
# $ python --version
# Python 3.7.3


from typing import List
from collections import defaultdict


class Edge:
    """Assume strict naming convention, 2 single character node labels and a weight
    example: input = AB5 OR input = AB500
    Let's ignore the lack of labels and assume we have only A-Z
    Assume weights are integer
    """
    def __init__(self, input: str):
        self.weight = int(input[2:])
        self.source = input[1]  # superfluous if use Graph._hashify
        self.destination = input[0]  # superfluous if use Graph._hashify


class Graph:
    def __init__(self, edges: List[str] = []):
        self.edges = edges
        self.graph = defaultdict(list)  # avoid key errors
        self.hashTable = defaultdict(Edge)  # avoid key errors
        self.visited = defaultdict(bool)
        self._hashify()
        self._graphify()
        self._trackVisited()

    """build a hash table to avoid O(N^2) operations, may come in handy
    It has O(1) average, minor rehash op
    lets keep it flat and put only weights as values
    """
    def _hashify(self):
        for edge in self.edges:
            self.hashTable[edge[:2]] = Edge(edge)

    """Notes: Some arbitrarily expensive op when adding an edge to existing graph
    one must also extend the hash table, check edge from self.edges
    in this task, I would opt out of doing any hash table, but I
    did question 1 before question 2, and did not optimize. :)
    So for simplicity, assume this method is private and only accessed
    in __init__
    """
    def _addEdge(self, source, destination):
        if self.graph[source]:
            self.graph[source].append(
                destination
            )  # Question: am I able to append to a None?
        else:
            self.graph[source] = [destination]

    def _graphify(self):
        for edge in self.edges:
            self._addEdge(edge[0], edge[1])

    def _trackVisited(self):
        for edge in self.edges:
            # edge counting blindly
            self.visited[edge[0]] = False
            self.visited[edge[1]] = False

    def _clearVisits(self):
        # clearing 'visited' with n+n space
        self.visited = dict.fromkeys(self.visited, 0)

    """
    It is asymptotically faster to first build a hash table,
    avoid an arbitrarily large list search of O(N^2) time,
    by doing an O(N) operation instead then accessing each edge
    in a hash table becomes an O(1) operation, which to find
    the path would be a worst case N time aka O(N)

    Given path, find the exact distance of this fixed path
    """
    def computeExactPathDistance(self, path: str):
        """To avoid dubious cleanup, lets assume 'path' input
        have no '-' separators, nevermind about path.replace('-', ''),
        assume path[0] is source, path[-1] is destination.

        We also assume we want the exact path given in 'path' parameter,
        we're not computing shortest here.

        e.g. edges = [AB3, BC2, CD5], computeExactPathDistance(ABC)
        3 + 2 + 5 = 10, return 10
        """

        if not path:
            return 0

        # if edges are the same 'label', assume this is a ref to the same node
        if path[0] == path[-1]:
            return 0

        # access each path in the hash table, O(N) time of O(1) access ops
        # get the weight of said edge and move on
        index = 0
        distance = 0
        while index < len(path) - 1:
            edgeBubble = path[index: index + 2]
            edge = self.hashTable.get(edgeBubble)
            # bad path given, distance is irrelevant
            if not edge:
                return "NO SUCH ROUTE"
            distance += edge.weight
            index += 1

        return distance

    def _countAllUniquePathsByDFSHelper(
        self,
        current: str,
        destination: str,
        visited: bool,
        count: int,
        paths: List[str],
    ):

        # visit
        visited[current] = True
        paths.append(current)

        # completed a unique path
        if current == destination:
            count += 1
            print(paths) # debug by providing each unique path to STDOUT
        else:
            # this route is meant to be further explored
            for node in self.graph[current]:
                if visited[node] is None:
                    print(f"Error: node {node} is not in graph")
                elif not visited[node]:
                    count += self._countAllUniquePathsByDFSHelper(
                        node, destination, visited, count, paths
                    )

        # unvisit to allow this node to be revisited by another path
        paths.pop()
        visited[current] = False

        return count

    """Theoretically, we have DFS, BFS to choose from as most straightfwd,
    however DFS is dyamic programming based, while BFS is queue-based.
    BFS would apply a queue, generally a more straightforward approach
    for finding shortest path. DFS is a more exhaustive approach,
    ideal for count all possibilities and comparing to find best possible.
    So let's go with DFS.
    """
    def countAllUniquePathsByDFS(self, source: str, destination: str):
        # superfluous, but more practical case catching
        if source == destination:
            return 1

        # Gets total count from helper
        count = self._countAllUniquePathsByDFSHelper(
            source, destination, self.visited, 0, []
        )

        # clean up this instance
        self._clearVisits()

        return count

    """Find the shortest path between two nodes

    We can assume the weights are non-negative and use dikjstra's. However,
    following the theme of practicality, we will go with Bellman-Ford
    to allow negative weights to exist.
    """
    def findLengthOfShortestPathBetweenTwo(self, source: str, destination: str):
        length = 0

        # Bellman-Ford

        return 0


if __name__ == "__main__":
    """Normally as a python engineer, I would create a test file
    that tests the classes in a separate file folder. However,
    here I will do all my tests in the main to save some time.

    I created scenarios as a dictionary, it could easily be a class too.
    """

    """Assignment 1: Given any arbitrary array of nodes, path [],
    compute the distance of this path, dist num
    """
    edges = []
    g = Graph(edges)
    distance = g.computeExactPathDistance("")

    assert distance == 0

    scenario = {"edges": ["AB1", "BC2", "CD5"], "path": "ABCD", "expected": 8}
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])

    assert distance == scenario["expected"]

    scenario = {
        "edges": ["AB1", "BC2", "CD5", "DC4", "CE16"],
        "path": "ABCE",
        "expected": 19,
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])

    assert distance == scenario["expected"]

    print("All tests passed")

    """Leaving this here to show my thinking on expanding on the available tests
    typically, it is better to do unit tests
    """
    # for scenario in scenarios:
    #   g = new Graph(scenario.edges)
    #   g.computeExactPathDistance(scenario.path)

    """Assignment 2: All unique paths for node to node, aka search algorithm
    """

    scenario = {
        "edges": ["AB1", "BC2", "CD5", "DC4", "CE16"],
        "source": "A",
        "destination": "C",
        "expected": 1,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )

    assert pathsCount == scenario["expected"]

    scenario = {
        "edges": ["AB1", "BC2", "CD5", "DC4", "CE16"],
        "source": "A",
        "destination": "E",
        "expected": 1,  # Cannot revisit C
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )

    assert pathsCount == scenario["expected"]

    """Assignment 3: Find shortest path between two, aka dijkstra's / bellman-ford
    """