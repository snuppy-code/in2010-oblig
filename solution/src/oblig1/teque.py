import sys

n = int(sys.stdin.readline())

class Teque:
    def __init__(self) -> None:
        self._storage = []

    # O(n) i værste tilfelle. Hvis listen er "full" må n elementer kopieres når listen re-allokeres.
    def push_back(self, value: int) -> None:
        self._storage.append(value)

    # O(n) i værste tilfelle
    def push_front(self, value: int) -> None:
        self._storage.insert(0, value)

    # O(n) i værste tilfelle
    def push_middle(self, value: int) -> None:
        self._storage.insert((len(self) + 1)//2, value)

    # O(1) i værste tilfelle
    def get(self, index: int) -> int:
        return self._storage[index]

    def __len__(self):
        return len(self._storage)


queue = Teque()

for line in sys.stdin:
    command, value = line.split(" ")
    value = int(value)

    if command == "get":
        print(queue.get(value))

    elif command == "push_back":
        queue.push_back(value)

    elif command == "push_front":
        queue.push_front(value)

    elif command == "push_middle":
        queue.push_middle(value)
