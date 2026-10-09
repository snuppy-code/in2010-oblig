import heapq
import sys
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from operator import add
from typing import Any, override


class Graph:
    def __init__(self):
        self._nodes = dict()
        self._edges = dict()

    def add_node(self, node):
        self._nodes[node.get_id()] = node

    def add_edge(self, u_id, v_id):
        assert u_id in self._nodes and v_id in self._nodes

        self._edges.setdefault(u_id, []).append(self._nodes[v_id])
        self._edges.setdefault(v_id, []).append(self._nodes[u_id])

    def is_connected(self, u, v):
        u_neighbors = self._edges[u.get_id()]
        v_neighbors = self._edges[v.get_id()]

        if v in u_neighbors:
            assert u in v_neighbors
        if u in v_neighbors:
            assert v in u_neighbors

        return u in v_neighbors

    def get_neighbors(self, u):
        id = u.get_id()
        if id in self._edges:
            return self._edges[id]
        else:
            return []

    def print_skuespiller_komponenter(self, componenter):
        componenter_output = dict()

        for v in componenter:
            if v in componenter_output:
                componenter_output[v] += 1
            else:
                componenter_output[v] = 1

        print(len(componenter_output))

        for k, v in componenter_output.items():
            print(f"There are {v} components of size {k}")

    def skuespiller_komponenter_bfsfull(self):
        visited = set()
        components = []
        for v in self._nodes.values():
            if v not in visited:
                size = self._skuespiller_bfs_visit(v, visited)
                if size == 0:
                    continue
                components.append(size)
        return components

    def _skuespiller_bfs_visit(self, s, visited):
        size = 0
        visited.add(s)
        queue = deque()
        queue.append(s)
        while len(queue) > 0:
            u = queue.popleft()
            if isinstance(u, Skuespiller):
                size += 1
            for v in self.get_neighbors(u):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        return size

    def print_sixdegrees(self, path):
        print("\t".join(path))

    def sixdegrees_bfs_visit(self, nmid1, nmid2):
        s = self._nodes[nmid1]
        addedby = dict()
        addedby[s] = None
        queue = deque()
        queue.append(s)
        while len(queue) > 0:
            u = queue.popleft()
            for v in self.get_neighbors(u):
                if v not in addedby:
                    addedby[v] = u
                    if v.get_id() == nmid2:
                        path = []
                        curr = v
                        while curr is not None:
                            path.append(curr.get_id())
                            curr = addedby[curr]
                        debug(nmid1, nmid2)
                        debug("\t".join(reversed(path)))
                        return reversed(path)
                    queue.append(v)

    def print_chillestevei(self, path):
        print("\t".join(path))

    def chillestevei_dijkstra(self, nmid1, nmid2):
        debug(nmid1, nmid2)

        s = self._nodes[nmid1]

        addedby = dict()
        addedby[s] = None
        queue = []
        heapq.heappush(queue, PrioritizedNode(priority=0, item=s))

        while len(queue) > 0:
            u = heapq.heappop(queue)

            for v in self.get_neighbors(u.item):
                if v in addedby:
                    continue

                addedby[v] = u.item

                weight = u.priority
                if isinstance(v, Film):
                    weight += 10 - v.get_rating()

                if v.get_id() == nmid2:
                    path = []
                    curr = v
                    while curr is not None:
                        path.append(curr.get_id())
                        curr = addedby[curr]
                    debug(nmid1, nmid2)
                    debug("\t".join(reversed(path)))
                    return reversed(path)
                # debug(f"adding {v} with priority {weight}")
                heapq.heappush(queue, PrioritizedNode(priority=weight, item=v))
                # debug(queue)

        assert False, "Unreachable!"


@dataclass(order=True)
class PrioritizedNode:
    priority: int
    item: Any = field(compare=False)


class Node(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    def __str__(self):
        return self.get_id()


class Film(Node):
    def __init__(self, tittel, tt_ID, rating):
        super().__init__()
        rating = float(rating)
        assert 10 >= rating >= 0, "creating film with disallowed rating range"
        self._tittel = tittel
        self._tt_ID = tt_ID
        self._rating = rating

    @override
    def get_id(self):
        return self._tt_ID

    def get_rating(self):
        return self._rating


class Skuespiller(Node):
    def __init__(self, navn, nm_ID):
        super().__init__()
        self._navn = navn
        self._nm_ID = nm_ID

    @override
    def get_id(self):
        return self._nm_ID


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    db = Graph()

    M = int(input())
    for i in range(M):
        parts = input().split("\t")
        # parts består av [ttid, tittel, rating]
        ttid, tittel, rating = parts
        db.add_node(Film(tittel, ttid, rating))

    A = int(input())
    for i in range(A):
        parts = input().split("\t")
        # parts består av [id, navn]
        id, navn = parts
        db.add_node(Skuespiller(navn, id))

    E = int(input())
    for i in range(E):
        parts = input().split("\t")
        # parts består av [ttid, nmid]
        ttid, nmid = parts
        db.add_edge(ttid, nmid)

    # Finn komponenter
    db.print_skuespiller_komponenter(db.skuespiller_komponenter_bfsfull())

    Qs = int(input())
    for i in range(Qs):
        parts = input().split("\t")
        # parts består av [nmid₁, nmid₂]
        nmid_1, nmid_2 = parts
        db.print_sixdegrees(db.sixdegrees_bfs_visit(nmid_1, nmid_2))

    # Finn korteste vei og print ut på en linje

    Qc = int(input())
    for i in range(Qc):
        parts = input().split("\t")
        # parts består av [nmid₁, nmid₂]
        nmid1, nmid2 = parts
        debug(parts)
        db.print_chillestevei(db.chillestevei_dijkstra(nmid1, nmid2))


# Finn chilleste vei og print ut på en linje

main()
