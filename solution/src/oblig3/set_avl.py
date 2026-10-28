import sys
from typing import Optional

def debug(*args, **kwargs):
    print(file=sys.stderr, *args, **kwargs)

def main():
    N = int(input())
    set = SetAvl()
    for _ in range(N):
        command = input().split()
        if command[0] == "contains":
            print(str(set.contains(int(command[1]))).lower())

        if command[0] == "insert":
            set.insert(int(command[1]))

        if command[0] == "remove":
            set.remove(int(command[1]))

        if command[0] == "size":
            print(set.size())


class AvlNode:
    def __init__(self, value: int, depth: int, parent: Optional[AvlNode] = None):
        self.depth: int = depth
        self.children: int = 0
        self.height = 1


        self.value = value
        self.left: Optional["AvlNode"] = None
        self.right: Optional["AvlNode"] = None
        self.parent: Optional["AvlNode"] = parent

    def insert(self, x: int):
        if self.value == x:
            return

        if self.value > x:
            if self.left is None:
                self.children += 1
                self.left = AvlNode(x, self.depth + 1, self)
            else:
                self.left.insert(x)
        elif self.value < x:
            if self.right is None:
                self.children += 1
                self.right = AvlNode(x, self.depth + 1, self)
            else:
                self.right.insert(x)

        self.update_children()

    def update_children(self):
        t = 0
        if self.right is not None:
            t += self.right.children + 1
        if self.left is not None:
            t += self.left.children + 1

        self.children = t

    def remove(self, x: int):
        if x < self.value:
            if self.left is not None:
                self.left = self.left.remove(x)
                self.update_children()
            return self

        if x > self.value:
            if self.right is not None:
                self.right = self.right.remove(x)
                self.update_children()
            return self

        if self.parent is not None:
            self.parent.children -= 1

        if self.left is None:
            return self.right
        if self.right is None:
            return self.left

        min = self.right
        while min.left is not None:
            min = min.left

        if min is not None:
            self.value = min.value
            self.right = self.right.remove(min.value)

        self.update_children()
        return self



    def find_child(self, x: int) -> Optional["AvlNode"]:
        if self.value == x:
            return self

        elif self.value > x:
            if self.left is None:
                return None
            return self.left.find_child(x)
        elif self.value < x:
            if self.right is None:
                return None
            return self.right.find_child(x)

        assert False, "should not happen"


class SetAvl:
    def __init__(self):
        self._root: Optional[AvlNode] = None

    def contains(self, x):
        if self._root is None:
            return False

        return self._root.find_child(x) is not None

    def insert(self, x):
        if self._root is None:
            self._root = AvlNode(x, 0)
        else:
            self._root.insert(x)

    def remove(self, x):
        self._root = self._root.remove(x)

    def size(self):
        if self._root is None:
            return 0
        return self._root.children + 1


if __name__ == '__main__':
    main()
