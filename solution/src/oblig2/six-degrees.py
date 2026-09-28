import heapq
import sys, collections
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import override, List, Optional, Dict, Tuple


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Representerer en node i grafen.
# Arver fra `ABC` (abstract base class), som blir tilsvarende en `abstract` klasse i Java.
class Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    def __str__(self) -> str:
        return self.get_id()

# Representerer en film i grafen
class Movie(Node):
    def __init__(self, ttid: str, title: str, rating: float):
        self.ttid = ttid
        self.title = title
        self.rating = rating

        super().__init__()

    @override
    def get_id(self):
        return self.ttid

# Representerer en skuespiller i grafen
class Actor(Node):
    def __init__(self, nmid: str, navn: str):
        self.nmid = nmid
        self.navn = navn
        super().__init__()

    @override
    def get_id(self):
        return self.nmid


# Brukes til i prioritetskøen i chillest_path.
# Stjålet fra dokumentasjonen til `heapq`: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
@dataclass(order=True)
class ChillestPathQueueItem:
    total_weight: float
    node_id: str = field(compare=False)

# representerer grafen
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


    def compute_components(self) -> Tuple[int, Dict[int, int]]:
        visited = set()

        # mapper (antall `Actor`s i komponentet) -> (antall komponenter med så mange `Actor`s)
        component_map: Dict[int, int] = dict()

        for _, n in self._nodes.items():
            # hopper over noder som allerede har blit telt
            if n in visited:
                continue
            elements_in_component = self.dfs_iterative(n, visited)

            # hvis vi starter å utforske fra en Movie node kan det hende at dfs_iterative returnerer 0
            # de telles ikke med i det endelige resultatet
            if elements_in_component == 0:
                continue

            if elements_in_component in component_map:
                component_map[elements_in_component] += 1 # øker antallet
            else:
                component_map[elements_in_component] = 1 # eller setter til 1 om det antallet ikke har blitt sett før

        return len(component_map.keys()), component_map

    def shortest_path(self, src: str, dst: str):
        src_node = self.get_node_by_id(src)

        visited = {src_node}
        queue = collections.deque()
        queue.append(src_node)

        node_shortest_path_to: Dict[str, Optional[str]] = {n: None for n in self._nodes}

        while len(queue) > 0:
            node = queue.popleft()

            for neighbour in self._edge_map[node.get_id()]:
                if not neighbour in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)

                    node_shortest_path_to[neighbour.get_id()] = node.get_id()

                    if neighbour.get_id() == dst:
                        path = [dst]
                        next = node_shortest_path_to[dst]
                        while next is not None:
                            path.append(next)
                            next = node_shortest_path_to[next]

                        return reversed(path)




        return None

    def chillest_path(self, src: str, dst: str) -> Optional[List[str]]:
        queue: List[ChillestPathQueueItem] = []
        visited = set()

        node_shortest_path_to: Dict[str, Optional[str]] = {n: None for n in self._nodes}

        src_node = self.get_node_by_id(src)
        heapq.heappush(queue, ChillestPathQueueItem(total_weight=0.0, node_id=src))
        visited.add(src)

        while len(queue) > 0:
            item = heapq.heappop(queue)

            for neighbour in self._edge_map[item.node_id]:
                if not neighbour.get_id() in visited:
                    # debug(f"visiting {neighbour.get_id()} from {item.node_id}")
                    new_weight = item.total_weight
                    visited.add(neighbour.get_id())
                    # new_path = [*item.path, item.node_id]


                    if isinstance(neighbour, Movie):
                        new_weight += 10.0 - neighbour.rating

                    heapq.heappush(queue, ChillestPathQueueItem(total_weight=new_weight, node_id=neighbour.get_id()))

                    node_shortest_path_to[neighbour.get_id()] = item.node_id

                    if neighbour.get_id() == dst:
                        # debug(node_shortest_path_to)
                        path = [dst]
                        next = node_shortest_path_to[dst]
                        while next is not None:
                            path.append(next)
                            next = node_shortest_path_to[next]

                        return reversed(path)


        return None

    # rekursiv implementasjon av depth-first search som teller antall `Actor`s den finner
    # ikke brukt i det ferdige programmet, siden det fulle datasettet krasher med RecursionError: maximum recursion depth exceeded
    def dfs_recursive(self, n: Node, visited: set) -> int:
        visited.add(n)
        sum = 1 if isinstance(n, Actor) else 0
        for neighbour in self._edge_map[n.get_id()]:
            if not neighbour in visited:
                sum += self.dfs_recursive(neighbour, visited)

        return sum

    # iterativ implementasjon av DFS teller antall `Actor`s den finner i dette komponentet
    def dfs_iterative(self, n: Node, visited: set) -> int:
        queue = collections.deque()
        queue.append(n)

        actor_count = 1 if isinstance(n, Actor) else 0

        while len(queue) > 0:
            node = queue.popleft()

            for neighbour in self._edge_map[node.get_id()]:
                if neighbour in visited:
                    continue

                if isinstance(neighbour, Actor):
                    actor_count += 1
                visited.add(neighbour)
                queue.append(neighbour)

        return actor_count


def main():
    graph = Graph()

    M = int(input())
    debug(f"adding {M} movies")
    for i in range(M):
        ttid, title, rating = input().split("\t");
        # parts består av [ttid, tittel, rating]

        graph.add_node(Movie(ttid, title, float(rating)))

    debug("added all movies")

    A = int(input())
    for i in range(A):
        nmid, navn = input().split("\t")
        graph.add_node(Actor(nmid, navn))

    debug("added all actors")

    E = int(input())
    for i in range(E):
        src, dst = input().split("\t")
        src = graph.get_node_by_id(src)
        dst = graph.get_node_by_id(dst)
        graph.add_edge(src, dst)

    debug("added all edges")

    # Finn komponenter
    component_count, component_map = graph.compute_components()
    print(component_count)
    for k, v in component_map.items():
        print(f"There are {v} components of size {k}")

    debug("finished finding components")

    Qs = int(input())
    for i in range(Qs):
        src, dst = input().split("\t");
        # parts består av [nmid₁, nmid₂]

        print("\t".join(graph.shortest_path(src, dst)))

    debug("finished finding shortest paths")

    Qc = int(input())
    for i in range(Qc):
        src, dst = input().split("\t");
        # parts består av [nmid₁, nmid₂]

        path = graph.chillest_path(src, dst)
        # debug("\t".join(path))
        print("\t".join(path))

    debug("finished finding chillest paths")

main()
