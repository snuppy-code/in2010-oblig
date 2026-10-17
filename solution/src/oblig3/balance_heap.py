import heapq
import sys

def main():
    heap = PriorityQueue()
    for line in sys.stdin:
        heap.insert(int(line))

    print_balanced(heap)

def print_balanced(heap):
    pass  # Løs oppgaven her

class PriorityQueue:
    def __init__(self):
        self._items = []

    def insert(self, value):
        heapq.heappush(self._items, value)

    def removemin(self, value):
        return heapq.heappop(self._items)

    def peek(self):
        return self._items[0]

    def size(self):
        return len(self._items)

if __name__ == '__main__':
    main()
