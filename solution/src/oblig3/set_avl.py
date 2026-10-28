import collections
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
    def __init__(self, value: int):
        self.children: int = 0
        self.height: int = 0

        self.value = value
        self.left: Optional["AvlNode"] = None
        self.right: Optional["AvlNode"] = None

    @classmethod
    def insert(cls, node: "AvlNode", x: int):
        if node.value == x:
            return node

        if node.value > x:
            if node.left is None:
                node.children += 1
                node.left = AvlNode(x)
            else:
                node.left = AvlNode.insert(node.left, x)
        elif node.value < x:
            if node.right is None:
                node.children += 1
                node.right = AvlNode(x)
            else:
                node.right = AvlNode.insert(node.right, x)

        node._update_height()
        node = AvlNode._balance(node)
        node._update_children()
        return node

    def _update_children(self):
        t = 0
        if self.right is not None:
            t += self.right.children + 1
        if self.left is not None:
            t += self.left.children + 1

        self.children = t

    @classmethod
    def remove(cls, node: "AvlNode", x: int):
        if x < node.value:
            if node.left is not None:
                node.left = AvlNode.remove(node.left, x)
                node._update_children()
            return node

        if x > node.value:
            if node.right is not None:
                node.right = AvlNode.remove(node.right, x)
                node._update_children()
            return node

        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        min = node.right
        while min.left is not None:
            min = min.left

        if min is not None:
            node.value = min.value
            node.right = AvlNode.remove(node.right, min.value)

        node._update_height()
        node = AvlNode._balance(node)
        node._update_children()
        return node

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

        assert False, "should not happen with given test data"

    def _balance_factor(self):
        left = -1 if self.left is None else self.left.height
        right = -1 if self.right is None else self.right.height
        return left - right

    @classmethod
    def _balance(cls, node: "AvlNode"):
        bf = node._balance_factor()
        if bf < -1:
            if node.right._balance_factor() > 0:
                node.right = AvlNode._rotate_right(node.right)
            return AvlNode._rotate_left(node)
        if bf > 1:
            if node.left._balance_factor() < 0:
                node.left = AvlNode._rotate_left(node.left)
            return AvlNode._rotate_right(node)
        return node

    @classmethod
    def _rotate_left(cls, node: "AvlNode"):
        y = node.right
        t1 = y.left

        y.left = node
        node.right = t1
        node._update_height()
        node._update_children()
        y._update_height()
        y._update_children()

        return y

    @classmethod
    def _rotate_right(cls, node: "AvlNode"):
        y = node.left
        t1 = y.right

        y.right = node
        node.left = t1
        node._update_height()
        node._update_children()
        y._update_height()
        y._update_children()

        return y

    def _update_height(self):
        left = -1 if self.left is None else self.left.height
        right = -1 if self.right is None else self.right.height
        self.height = 1 + max(left, right)


class SetAvl:
    def __init__(self):
        self._root: Optional[AvlNode] = None

    def contains(self, x):
        if self._root is None:
            return False

        return self._root.find_child(x) is not None

    def insert(self, x):
        if self._root is None:
            self._root = AvlNode(x)
        else:
            self._root = AvlNode.insert(self._root, x)

    def remove(self, x):
        if self._root is not None:
            self._root = AvlNode.remove(self._root, x)

    def size(self):
        if self._root is None:
            return 0
        return self._root.children + 1


if __name__ == '__main__':
    main()
