import sys, collections
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import override, List


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    def __str__(self) -> str:
        return self.get_id()

class Movie(Node):
    def __init__(self, ttid: str, title: str, rating: float):
        self.ttid = ttid
        self.title = title
        self.rating = rating

        super().__init__()

    @override
    def get_id(self):
        return self.ttid

class Actor(Node):
    def __init__(self, id: str, navn: str):
        self.nmid = id
        self.navn = navn
        super().__init__()

    @override
    def get_id(self):
        return self.nmid



class Graph:
    def __init__(self):
        self._nodes = dict()
        self._edge_map = dict()

    def add_node(self, n: Node):
        self._nodes[n.get_id()] = n
        self._edge_map[n.get_id()] = []

    def add_edge(self, src: Node, dst: Node):
        self._edge_map[src.get_id()].append(dst)
        self._edge_map[dst.get_id()].append(src)

    def get_node_by_id(self, id: str):
        return self._nodes[id]

    def compute_components(self):
        visited = set()
        count = 0

        map = dict()
        for _, n in self._nodes.items():
            if not n in visited:
                count += 1
                elements_in_components = self.dfs_recursive(n, visited)
                if elements_in_components in map:
                    map[elements_in_components] += 1
                else:
                    map[elements_in_components] = 1

        return count, map

    def shortest_path(self, src: str, dst: str):
        visited = set()
        queue = collections.deque()

        queue.append((self.get_node_by_id(src), []))


        while len(queue) > 0:
            node, path_to  = queue.popleft()

            for neighbour in self._edge_map[node.get_id()]:
                if not neighbour in visited:
                    queue.append((neighbour, [*path_to, node]))
                    visited.add(neighbour)

                    if neighbour.get_id() == dst:
                        return [x.get_id() for x in [*path_to, node, neighbour]]

        return []

    def chillest_path(self):


    def dfs_recursive(self, n: Node, visited: set) -> int:
        visited.add(n)
        sum = 1 if isinstance(n, Actor) else 0
        for neighbour in self._edge_map[n.get_id()]:
            if not neighbour in visited:
                sum += self.dfs_recursive(neighbour, visited)

        return sum

def main():

    graph = Graph()

    M = int(input())
    for i in range(M):
        ttid, title, rating = input().split("\t");
        # parts består av [ttid, tittel, rating]

        graph.add_node(Movie(ttid, title, float(rating)))

    A = int(input())
    for i in range(A):
        nmid, navn = input().split("\t")
        graph.add_node(Actor(nmid, navn))

    E = int(input())
    for i in range(E):
        src, dst = input().split("\t")
        src = graph.get_node_by_id(src)
        dst = graph.get_node_by_id(dst)
        graph.add_edge(src, dst)

    # Finn komponenter
    component_count, component_map = graph.compute_components()
    print(component_count)
    for k, v in component_map.items():
        print(f"There are {v} components of size {k}")

    Qs = int(input())
    for i in range(Qs):
        src, dst = input().split("\t");
        # parts består av [nmid₁, nmid₂]

        print("\t".join(graph.shortest_path(src, dst)))

    Qc = int(input())
    for i in range(Qc):
        parts = input().split("\t");
        # parts består av [nmid₁, nmid₂]

        # Finn chilleste vei og print ut på en linje

main()
