import heapq
import sys, collections
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import override, List, Optional, Dict, Tuple, Iterable


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

    def add_edge(self, src: str, dst: str):
        self._edge_map[src].append(dst)
        self._edge_map[dst].append(src)

    def get_node_by_id(self, id: str):
        return self._nodes[id]


    def compute_components(self) -> Tuple[int, Dict[int, int]]:
        visited = set()

        # mapper (antall `Actor`s i komponentet) -> (antall komponenter med så mange `Actor`s)
        component_map: Dict[int, int] = dict()

        for node_id in self._nodes:
            # hopper over noder som allerede har blit telt
            if node_id in visited:
                continue
            elements_in_component = self.dfs_iterative(node_id, visited)

            # hvis vi starter å utforske fra en Movie node kan det hende at dfs_iterative returnerer 0
            # de telles ikke med i det endelige resultatet
            if elements_in_component == 0:
                continue

            if elements_in_component in component_map:
                component_map[elements_in_component] += 1 # øker antallet
            else:
                component_map[elements_in_component] = 1 # eller setter til 1 om det antallet ikke har blitt sett før

        return len(component_map.keys()), component_map

    def shortest_path(self, src: str, dst: str) -> Iterable[str]:
        visited = {src}
        queue = collections.deque()
        queue.append(src)

        added_by: Dict[str, Optional[str]] = {n: None for n in self._nodes}

        while len(queue) > 0:
            node = queue.popleft()
            for neighbour in self._edge_map[node]:
                if not neighbour in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)

                    added_by[neighbour] = node

                    if neighbour == dst:
                        path = [dst]
                        next = added_by[dst]
                        while next is not None:
                            path.append(next)
                            next = added_by[next]

                        return reversed(path)

        # alle gitte spørringer finner alltid en gyldig vei
        raise RuntimeError("should not happen")

    def chillest_path(self, src: str, dst: str) -> Iterable[str]:
        # sorteres alltid slik at veien med lavest total_weight alltid er først
        queue: List[ChillestPathQueueItem] = []
        visited = {src}

        # map fra node_id -> node_id til den noden som kommer før denne i veien
        # brukes til å holde styr på den chilleste veien
        # kan lett traverseres for å finne hele veien
        # blir som et slags ukomplett spenntre(?)
        added_by: Dict[str, Optional[str]] = {n: None for n in self._nodes}

        heapq.heappush(queue, ChillestPathQueueItem(total_weight=0.0, node_id=src))

        while len(queue) > 0:
            item = heapq.heappop(queue)

            for neighbour in self._edge_map[item.node_id]:
                if neighbour in visited:
                    continue

                visited.add(neighbour)

                neighbour_node = self.get_node_by_id(neighbour)
                new_weight = item.total_weight
                if isinstance(neighbour_node, Movie):
                    new_weight += 10.0 - neighbour_node.rating # oppdatere total_weight hvis vi går til en ny film

                heapq.heappush(queue, ChillestPathQueueItem(total_weight=new_weight, node_id=neighbour))

                # den korteste veien til noden `neighbour` må være fra `item.node_id`
                added_by[neighbour] = item.node_id

                # hvis vi har kommet til slutten konstrueres og returneres veien
                if neighbour == dst:
                    # går baklengs gjennom added_by for å finne veien
                    path = [dst]
                    next = added_by[dst]
                    while next is not None:
                        path.append(next)
                        next = added_by[next]

                    return reversed(path)

        # alle gitte spørringer finner alltid en gyldig vei
        raise RuntimeError("should not happen")

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
    def dfs_iterative(self, n: str, visited: set) -> int:
        queue = collections.deque()
        queue.append(n)

        actor_count = 1 if isinstance(self.get_node_by_id(n), Actor) else 0

        while len(queue) > 0:
            node = queue.popleft()

            for neighbour in self._edge_map[node]:
                if neighbour in visited:
                    continue

                if isinstance(self.get_node_by_id(neighbour), Actor):
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
