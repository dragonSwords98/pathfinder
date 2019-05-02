import pytest
from pathfinder import Edge, Graph

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

    scenario = { #5
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
    scenario = { #1
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

    scenario = { #2
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

    scenario = { #3
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

    scenario = { #4
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
"""

def test_countAllUniquePathsByDFS_empty():
    scenario = {
        "edges": [],
        "source": "A", # dont-care
        "destination": "C", # dont-care
        "expected": 0,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsByDFS_no_answer_returns_zero():
    scenario = {
        "edges": ["AB2"],
        "source": "A",
        "destination": "C",
        "expected": 0,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )

    assert pathsCount == scenario["expected"]

    scenario = {
        "edges": ["AB2", "BD3", "DE4", "CA2"],
        "source": "A",
        "destination": "C",
        "expected": 0,
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )

    assert pathsCount == scenario["expected"]

def test_countAllUniquePathsByDFS_one_route():
    scenario = {
        "edges": ["AC1"],
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


def test_countAllUniquePathsByDFS_one_unique_path():
    pass


def test_countAllUniquePathsByDFS_loopback_in_path():
    scenario = {
        "edges": ["AB1", "BC2", "CD5", "DC4", "CE16"],
        "source": "A",
        "destination": "C",
        "expected": 2,
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
        "expected": 2,  # Can revisit C
    }
    g = Graph(scenario["edges"])
    pathsCount = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )

    assert pathsCount == scenario["expected"]


def test_countAllUniquePathsByDFS_less_or_equal_to():
    pass


def test_countAllUniquePathsByDFS_less():
    pass


def test_countAllUniquePathsByDFS_equal():
    scenario = { #7
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "source": "A",
        "destination": "C",
        "limit": 4,
        "notation": "==",
        "expected": 3,
    }
    g = Graph(scenario["edges"])
    distance = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
        scenario["limit"],
        scenario["notation"],
    )
    assert distance == scenario["expected"]


def test_countAllUniquePathsByDFS_greater_or_equal_to():
    pass


def test_countAllUniquePathsByDFS_greater():
    pass


def test_countAllUniquePathsByDFS_roundtrip():
    scenario = { #6
        "edges": [
            "AB5", "BC4", "CD8", "DC8",
            "DE6", "AD5", "CE2", "EB3",
            "AE7",
        ],
        "source": "C",
        "destination": "C",
        "expected": 2,
    }
    g = Graph(scenario["edges"])
    distance = g.countAllUniquePathsByDFS(
        scenario["source"],
        scenario["destination"],
    )
    assert distance == scenario["expected"]


def test_countAllUniquePathsByDFS_many_paths():
    pass


# Assignment 3
"""Assignment 3: Find shortest path between two,
aka dijkstra's / bellman-ford
"""

def test_findLengthOfShortestPathBetweenTwo_empty():
    pass


def test_findLengthOfShortestPathBetweenTwo_no_answer():
    pass


def test_findLengthOfShortestPathBetweenTwo_short():
    pass


def test_findLengthOfShortestPathBetweenTwo_long():
    pass
