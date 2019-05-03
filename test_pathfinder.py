from pathfinder import Graph

"""Unit tests for pathfinder.py

Notes: Ideally, splitting test cases can be written into classes and
handled in bulk test suites. It is not ideal to 'loop assertions',
so I have laid out each assertion in explicit manner for legibility.
Assignments should have separate test files for file-folder clarity.
However, with time constraints, I will simplify my layout.

Edge case not covered: single-node network, we assume this is not
legal because the inputs have to be at least 2 towns + a distance.

Which also means we dont need to test 'AB2' for single B-B route,
because this is also impossible.
"""

"""Assignment 1: Given any arbitrary array of nodes, path [],
compute the distance of this path, dist num
"""


def test_computeExactPathDistance_empty():
    edges = []
    g = Graph(edges)
    distance = g.computeExactPathDistance("")

    assert distance == 0


def test_computeExactPathDistance_no_answer():
    scenario = {
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "BB",
        "expected": 'NO SUCH ROUTE',
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]

    scenario = {
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "BAB",
        "expected": 'NO SUCH ROUTE',
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]

    scenario = {
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "EBAEB",
        "expected": 'NO SUCH ROUTE',
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]

    scenario = {  # 5
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "AED",
        "expected": 'NO SUCH ROUTE',
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]


def test_computeExactPathDistance_small():
    scenario = {
        "edges": ["AB1", "BC2", "CD5"],
        "path": "ABCD",
        "expected": 8,
    }
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


def test_computeExactPathDistance_large():
    scenario = {  # 1
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "ABC",
        "expected": 9,
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]

    scenario = {  # 2
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "AD",
        "expected": 5,
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]

    scenario = {  # 3
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "ADC",
        "expected": 13,
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]

    scenario = {  # 4
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "path": "AEBCD",
        "expected": 22,
    }
    g = Graph(scenario["edges"])
    distance = g.computeExactPathDistance(scenario["path"])
    assert distance == scenario["expected"]


"""Assignment 2: All unique paths for node to node,
aka search algorithm

Theoretically, we have DFS, BFS to choose from as most straightfwd,
however DFS is dyamic programming based, while BFS is queue-based.
BFS would apply a queue, generally a more straightforward approach
for finding shortest path. DFS is a more exhaustive approach,
ideal for count all possibilities and comparing to find best possible.

However, DFS requires a pointer in order to achieve the count in a recursive
approach. And queue allows me to better cover our limit/notation variants in
a simple if-tree, let's go with BFS.
"""


def test_countAllUniquePathsWithLimitByBFS_empty():
    scenario = {
        "edges": [],
        "source": "A",  # dont-care
        "destination": "C",  # dont-care
        "notation": '<=',
        "limit": 2,
        "expected": 0,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_no_answer_returns_zero():
    scenario = {
        "edges": ["AB2"],
        "source": "A",
        "destination": "C",
        "notation": '<=',
        "limit": 2,
        "expected": 0,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]

    scenario = {
        "edges": ["AB2", "BD3", "DE4", "CA2"],
        "source": "A",
        "destination": "C",
        "notation": '<=',
        "limit": 2,
        "expected": 0,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_one_route():
    scenario = {
        "edges": ["AC1"],
        "source": "A",
        "destination": "C",
        "notation": '<=',
        "limit": 2,
        "expected": 1,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_one_unique_path():
    scenario = {
        "edges": ["AB2", "BD3", "DC4", "CA2"],
        "source": "A",
        "destination": "C",
        "notation": '<=',
        "limit": 4,
        "expected": 1,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_loopback_in_path():
    scenario = {
        "edges": ["AB1", "BC2", "CD5", "DC4", "CE16"],
        "source": "A",
        "destination": "C",
        "notation": '<=',
        "limit": 5,
        "expected": 2,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]

    scenario = {
        "edges": ["AB1", "BC2", "CD5", "DC4", "CE16"],
        "source": "A",
        "destination": "E",
        "notation": '<=',
        "limit": 5,
        "expected": 2,  # Can revisit C
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_less_or_equal_to():
    scenario = {  # 6
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "source": "C",
        "destination": "C",
        "notation": '<=',
        "limit": 3,
        "expected": 2,
    }
    g = Graph(scenario["edges"])
    distance = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )
    assert distance == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_less():
    scenario = {
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "source": "C",
        "destination": "C",
        "notation": '<',
        "limit": 30,
        "expected": 3881,
    }
    g = Graph(scenario["edges"])
    distance = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )
    assert distance == scenario["expected"]


def test_countAllUniquePathsWithLimitByBFS_equal():
    scenario = {  # 7
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "source": "A",
        "destination": "C",
        "notation": "==",
        "limit": 4,
        "expected": 3,
    }
    g = Graph(scenario["edges"])
    distance = g.countAllUniquePathsWithLimitByBFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )
    assert distance == scenario["expected"]


# Assignment 3
"""Assignment 3: Find shortest path between two,
aka dijkstra's / bellman-ford.

We will use bellman-ford because we prefer not to assume
the weights are non-negative.
"""


def test_findLengthOfShortestPathBetweenTwo_empty():
    pass


def test_findLengthOfShortestPathBetweenTwo_no_answer():
    pass


def test_findLengthOfShortestPathBetweenTwo_short():
    pass


def test_findLengthOfShortestPathBetweenTwo_long():
    pass
