import collections  # For collections.deque.
import sys

n = int(sys.stdin.readline())

# De to interne dequene representerer første og andre halvdel av Teque dataene.
# Vi har en invariant: Første halvdel må alltid være like stor eller 1 større enn andre halvdel.
# Dette gjør at å push_back på første halvdel er det samme som å sette inn på index floor((k + 1)/2). Dette er hovedideen bak denne datastrukturen.
class Teque:
    def __init__(self) -> None:
        self._first_half = collections.deque()
        self._last_half = collections.deque()

    # O(n) i værste tilfelle, når de underliggende datastrukturene må utvides.
    # O(1) i de fleste tilfeller.
    # Samme som et vanlig dynamisk array.
    def push_front(self, value: int) -> None:
        self._first_half.appendleft(value)
        self._balance()

    # O(n) i værste tilfelle, når de underliggende datastrukturene må utvides.
    # O(1) i de fleste tilfeller.
    # Samme som et vanlig dynamisk array.
    def push_back(self, value: int) -> None:
        self._last_half.append(value)
        self._balance()

    # O(n) i værste tilfelle, når de underliggende datastrukturene må utvides.
    # O(1) i de fleste tilfeller.
    # Samme som et vanlig dynamisk array.
    def push_middle(self, value: int):
        self._first_half.append(value)
        self._balance()

    # O(1) i alle tilfeller.
    def get(self, i: int) -> None:
        if i >= len(self._first_half):
            return self._last_half[i-len(self._first_half)]
        elif i < len(self._first_half):
            return self._first_half[i]
        else:
            assert False, "Unreachable!" # burde aldri skje

    def _balance(self):
        balance = len(self._first_half) - len(self._last_half)

        if balance > 1:
            value = self._first_half.pop()
            self._last_half.appendleft(value)
        elif balance < 0:
            value = self._last_half.popleft()
            self._first_half.append(value)

    # debug lol
    def __str__(self):
        return f"{self._first_half!s}  {self._last_half!s}"




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
