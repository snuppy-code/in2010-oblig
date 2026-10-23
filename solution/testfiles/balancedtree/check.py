import sys
import typing as t

from dataclasses import dataclass
from argparse import ArgumentParser

@dataclass
class Node:
    element: int
    left: 'Node | None' = None
    right: 'Node | None' = None

def height(v: t.Optional[Node]) -> Node:
    return -1 if v is None else 1+max(height(v.left), height(v.right))

def insert(v: t.Optional[Node], x: int) -> Node:
    if v is None: return Node(x)
    if v.element < x: v.left = insert(v.left, x)
    if v.element > x: v.right = insert(v.right, x)
    return v

def min_height(v: t.Optional[Node]) -> int:
    return -1 if v is None else 1+min(min_height(v.left), min_height(v.right))

def is_balanced(v: t.Optional[Node]) -> bool:
    return height(v) - min_height(v) <= 1

def size(v: t.Optional[Node]):
    if v is None: return 0
    return size(v.left) + size(v.right) + 1


def is_avl(t: t.Optional[Node]) -> int | None:
    """
    returns the heigh of the tree if it is a valid AVL tree
    if it is not a valid AVL tree is None.

    The height of an empty tree (None) is considered to be one,
    so valid AVL trees will result in a truthy value
    """

    if t is None:
        return 1
    left = is_avl(t.left)
    right = is_avl(t.right)
    return left and right and abs(left-right) <= 1 and max(left, right) + 1

def to_set(t, s=None):
    if s is None:
        s = set()
    if t is not None:
        s.add(t.element)
        to_set(t.left, s)
        to_set(t.right, s)
    return s


def check(elements):
    tree = None
    for line in sys.stdin:
        if line.strip() == "": continue
        try:
            number = int(line)
        except NumberFormatException:
            print("Ugyldig output. pass på at programmet ditt ikke skriver ut "
                  "noe ekstra tekst")
            continue
        tree = insert(tree, number)

    if tree is None:
        print("Dette treet er tomt")
    elif not is_balanced(tree):
        if is_avl(tree):
            print("Dette treet er et gyldig avl tree, men ikke *helt balansert*.\n"
                  "Kravet i denne oppgaven er strengere enn for et avl-tre")
        else:
            print("Dette treet er ikke helt balansert")
    elif size(tree) != len(elements):
        print("Dette treet er balansert, men feil størrelse")
    elif to_set(tree) != elements:
        print("Dette treet er balansert, men har feil elementer")

if __name__ == '__main__':
    check({1, 2, 3})
