import heapq
import sys

def main():
    heap = PriorityQueue()
    for line in sys.stdin:
        heap.insert(int(line))

    print_balanced(heap)

def print_balanced(heap):
    if heap.size() == 0:
        return
    if heap.size() == 1:
        print(heap.removemin())
        return

    s = heap.size()
    to_pop = s // 2

    # gå til midten
    queue = PriorityQueue()
    for _ in range(to_pop):
        queue.insert(heap.removemin())

    # print midten
    print(heap.removemin())

    # print resten
    print_balanced(heap)
    print_balanced(queue)


    pass  # Løs oppgaven her

class PriorityQueue:
    def __init__(self):
        self._items = []

    def insert(self, value):
        heapq.heappush(self._items, value)

    def removemin(self):
        return heapq.heappop(self._items)

    def peek(self):
        return self._items[0]

    def size(self):
        return len(self._items)

if __name__ == '__main__':
    main()
