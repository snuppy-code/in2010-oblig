import sys
from typing import List, Optional

def debug(*args, **kwargs):
    pass
    # print(file=sys.stderr, *args, **kwargs)

# markerer en plass i arrayet som slettet
class Deleted:
    pass


def main():
    N = int(input())
    set = SetHash()
    for _ in range(N):
        command = input().split()
        if command[0] == "contains":
            out = str(set.contains(int(command[1]))).lower()
            print(out)
            debug(out)


        if command[0] == "insert":
            set.insert(int(command[1]))

        if command[0] == "remove":
            set.remove(int(command[1]))

        if command[0] == "size":
            print(set.size())
            debug(set.size())

# Bruker linear probing med "marker plassen som slettet" strategien for å håndtere sletting
class SetHash:
    def __init__(self):
        self._items: List[Optional[int | Deleted]] = [None] * 10
        self._size: int = 0
        self._capacity: int = 10

        self._test_set = set()

    def contains(self, x):
        i = x % self._capacity

        while self._items[i] is not None:
            if x == self._items[i]:
                assert x in self._test_set
                return True

            i = (i + 1) % self._capacity

        debug(f"{x} not in set. searched from {x % self._capacity}")

        assert (x not in self._test_set)
        return False

    def insert(self, x):
        self._test_set.add(x)

        if self.__loadfactor() > 0.5:
            debug("rehashing")
            self.__rehash()

        i = x % self._capacity

        while self._items[i] is not None:
            if self._items[i] == x:
                self.__assert_size()
                return
            i = (i + 1) % self._capacity

        self._items[i] = x
        self._size += 1
        debug(f"added {x} at {i} because {self._capacity}. new size {self._size}")
        self.__assert_size()

    def __loadfactor(self):
        return self._size / self._capacity

    def __rehash(self):
        old = [x for x in self._items if x is not None and not isinstance(x, Deleted)]
        self._capacity *= 2
        self._items = [None] * self._capacity

        for x in old:
            i = x % self._capacity

            while self._items[i] is not None:
                i = (i + 1) % self._capacity

            self._items[i] = x


    def __assert_size(self):
        assert len(self._test_set) == self.size(), f"expected size: {len(self._test_set)}. found {self.size()}"

    def remove(self, x):
        try:
            self._test_set.remove(x)
        except KeyError:
            pass

        i = x % self._capacity
        while self._items[i] is not None:
            if self._items[i] == x:
                debug(f"removing {x}")
                self._items[i] = Deleted()
                self._size -= 1
                self.__assert_size()
                return

            i = (i + 1) % self._capacity
        debug(f"{x} not in set. not removing")
        self.__assert_size()

    def size(self):
        return self._size

if __name__ == '__main__':
    main()
