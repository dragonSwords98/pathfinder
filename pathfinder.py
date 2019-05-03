# PathFinder.py
#
# Bryan Ling, courtesy of Receptiviti
#
# 2019-05-01


from typing import List
from collections import defaultdict, deque
import math

""" We wont use this exception but it's here
for an example where an error can be handled
# class NotationError(Exception):
#     pass
"""


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

    LEGAL_NOTATIONS = ["<", "<=", "=="]

    def __init__(self, edges: List[str] = []):
        self.edges = edges
        self.hashTable = defaultdict(Edge)  # avoid key errors
        self.graph = defaultdict(list)  # avoid key errors
        self.weightedGraph = []
        self._hashify()
        self._graphify()
        self.nodes = set()
        self._weightedGraphify()
        print(self.graph)

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
        self.graph[source].append(destination)

    def _addWeightedEdge(self, source, destination, weight):
        self.weightedGraph.append((source, destination, weight))

    def _weightedGraphify(self):
        for edge in self.edges:
            self.nodes.update(edge[:2])
            self._addWeightedEdge(edge[0], edge[1], edge[2])

    def _graphify(self):
        for edge in self.edges:
            self._addEdge(edge[0], edge[1])

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

        if len(path) == 2 and path[0] == path[-1]:
            # Assignment says impossible ¯\_(ツ)_/¯
            return "NO SUCH ROUTE"

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

    def _validateNotation(self, notation):
        """Assumptions made here about 'notation'.

        We assume notation will present legal operators only
        '<', '>', '==', '<=', '>='.

        Let's reject illegal operators that yield infinite loops.
        Reject: '>', '>=', etc.
        Accept: '<', ==', '<='

        Normally, an outer API layer will filter and provide
        proper 'if/else' or 'case' tree to validate the input.

        Without a notation, return False
        """
        if notation is None:
            return False

        return notation in self.LEGAL_NOTATIONS

    """ Simple mapping of nodes with the current limit
    """

    def _mapNeighborsWithLimit(self, neighbors: list, limit: int, path: list):
        enqueue = deque()
        for neighbor in neighbors:
            enqueue.append(
                {"node": neighbor, "limit": limit, "path": path + [neighbor]}
            )
        return enqueue

    """ Queue approach to count all unique paths by only going as deep
    as the limit for all breadths
    """

    def countAllUniquePathsWithLimitByBFS(
        self, source: str, destination: str, limit: int, notation: str = None
    ):
        if not self._validateNotation(notation):
            # typically we raise an exception
            # raise NotationError(f"{notation} is not a valid notation")
            return f"NotationError {notation} is not a valid notation"

        count = 0
        paths = []
        queue = self._mapNeighborsWithLimit(
            self.graph[source],
            limit - 1,
            [source],
        )

        while queue:  # O(|V * E|) op
            node = queue.popleft()
            current = node["node"]
            current_limit = node["limit"] - 1
            path = node["path"]

            # Equal case
            if notation == "==":  # exactly 'limit' stops
                if current == destination and current_limit == -1:
                    if path not in paths:
                        count += 1
                        paths.append(path)
                        # print(path) # debug
                        path = [source]
                if current_limit >= 0:
                    queue.extend(
                        self._mapNeighborsWithLimit(
                            self.graph[current], current_limit, path
                        )
                    )
            elif notation == "<=":  # maximum of 'limit' stops
                # 'less or equal to' cases
                if current == destination:
                    if path not in paths:
                        count += 1
                        paths.append(path)
                        # print(path) # debug
                        path = [source]
                if current_limit >= 0:
                    queue.extend(
                        self._mapNeighborsWithLimit(
                            self.graph[current], current_limit, path
                        )
                    )
            elif notation == "<":  # less than 'limit' stops
                # 'Less than' case
                if current == destination:
                    if path not in paths:
                        count += 1
                        paths.append(path)
                        # print(path) # debug
                        path = [source]
                if current_limit > 0:
                    queue.extend(
                        self._mapNeighborsWithLimit(
                            self.graph[current], current_limit, path
                        )
                    )
            # else # dont care

        return count

    """Find the shortest path between two nodes

    We can assume the weights are non-negative and use dikjstra's. However,
    following the theme of practicality, we will go with Bellman-Ford
    to allow negative weights to exist and throw exception for negative
    weight cycles
    """

    def _bellmanFord(
        self,
        source: str,
        destination: str,
    ):
        # set all node distances from source to infinity
        distances = dict.fromkeys(self.nodes, math.inf)
        distances[source] = 0

        sourceIsDestination = source == destination
        print('special case? ', sourceIsDestination)

        # relaxation is equal to the longest possible
        # shortest path which is `len(nodes) - 1`
        for relax in range(len(self.nodes) - 1):
            for (u, v, w) in self.weightedGraph:
                # special case where source is destination
                # override distance of source once
                if distances[u] != math.inf and v == destination and sourceIsDestination:
                    sourceIsDestination = False
                    distances[v] = distances[u] + int(w)
                elif distances[u] != math.inf and distances[u] + int(w) < distances[v]:
                    # if distance of source is not infinity (not reached yet)
                    # and that distance + weight of u-v is smaller than recorded
                    # distance[v], we've found a 'shorter path' to v
                    distances[v] = distances[u] + int(w)
                
        # negative-weight cycle check
        for (u, v, w) in self.weightedGraph: 
            if distances[u] != math.inf and distances[u] + int(w) < distances[v]: 
                return f"NegativeCycleError: distance of {u} + {w}" \
                " is less than distance to {v}"

        print(distances)
        return distances

    def findLengthOfShortestPathBetweenTwo(
        self,
        source: str,
        destination: str,
    ):
        if not set([source, destination]) <= set(self.nodes):
            return "NO SUCH ROUTE"


        # Bellman-Ford for all distances from source
        return self._bellmanFord(source, destination)[destination]

    def countAllUniquePathsBelowWeight(
        self,
        source: str,
        destination: str,
        weight: int,
    ):
        if not set([source, destination]) <= set(self.nodes):
            return "NO SUCH ROUTE"

        count = 0
        paths = []
        queue = deque([(source, [source], weight)])
        # FIFO queue
        while queue:
            (current, path, remaining_weight) = queue.popleft()

            for neighbor in self.graph[current]:
                neighbor_weight = self.hashTable[current + neighbor].weight
                temp_path = path + [neighbor]
                temp_weight = remaining_weight - neighbor_weight
                # there's still some 'gas left in the tank'
                if neighbor_weight < remaining_weight:
                    queue.append((
                        neighbor,
                        temp_path,
                        temp_weight,
                    ))
                    # we've arrived!
                    if neighbor == destination:
                        print(weight - temp_weight, temp_path)
                        paths.append({ "weight": weight - temp_weight, "path": temp_path })
                        count += 1

        return count