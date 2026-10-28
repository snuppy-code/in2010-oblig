package oblig3;

import java.io.*;

class SetAvl {
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int N = Integer.parseInt(br.readLine());
    SetAvl set = new SetAvl();

    for (int i = 0; i < N; i++) {
      String[] line = br.readLine().split(" ");
      String cmd = line[0];

      if (cmd.equals("contains")) {
        System.out.println(set.contains(Integer.parseInt(line[1])));
      } else if (cmd.equals("insert")) {
        set.insert(Integer.parseInt(line[1]));
      } else if (cmd.equals("remove")) {
        set.remove(Integer.parseInt(line[1]));
      } else if (cmd.equals("size")) {
        System.out.println(set.size());
      }
    }
  }

  private class Tree {
    Node root = null;
    private int size = 0;

    private static class Node {
      Node left = null;
      Node right = null;
      int height = 0;
      int element;

      Node(int x) {
        this.element = x;
      }
    }

    private int getHeight(Node v) {
      if (v == null) {
        return -1;
      }
      return v.height;
    }

    private void setHeight(Node v) {
      if (v == null) {
        return;
      }
      v.height = 1 + Math.max(getHeight(v.left), getHeight(v.right));
    }

    private Node leftRotate(Node v) {
      Node x = v.right;
      Node y = x.left;

      x.left = v;
      v.right = y;

      setHeight(v);
      setHeight(x);

      return x;
    }

    private Node rightRotate(Node v) {
      Node x = v.left;
      Node y = x.right;

      x.right = v;
      v.left = y;

      setHeight(v);
      setHeight(x);

      return x;
    }

    private Node find(Node v, int x) {
      if (v == null) {
        return null;
      }

      if (x == v.element) {
        return v;
      }

      if (x < v.element) {
        return find(v.left, x);
      }

      return find(v.right, x);
    }

    private int balanceFactor(Node v) {
      if (v == null) {
        return 0;
      }
      return (getHeight(v.left) - getHeight(v.right));
    }

    private Node balance(Node v) {
      if (balanceFactor(v) < -1) {
        if (balanceFactor(v.right) > 0) {
          v.right = rightRotate(v.right);
        }
        return leftRotate(v);
      }

      if (balanceFactor(v) > 1) {
        if (balanceFactor(v.left) < 0) {
          v.left = leftRotate(v.left);
        }
        return rightRotate(v);
      }

      return v;
    }

    boolean contains(int x) {
      return (!(find(root, x) == null));
    }

    Node insert(Node v, int x) {
      if (v == null) {
        size++;
        return new Node(x);
      }

      if (x < v.element) {
        v.left = insert(v.left, x);

      } else if (x > v.element) {
        v.right = insert(v.right, x);
      }

      setHeight(v);
      return balance(v);
    }

    private Node findMin(Node v) {
      if (v.left == null) {
        return v;
      }

      return findMin(v.left);
    }

    Node remove(Node v, int x) {
      if (v == null) {
        return null;
      }

      if (x < v.element) {
        v.left = remove(v.left, x);

      } else if (x > v.element) {
        v.right = remove(v.right, x);

      } else if (v.left == null) {
        v = v.right;
        size--;

      } else if (v.right == null) {
        v = v.left;
        size--;

      } else {
        Node u = findMin(v.right);
        v.element = u.element;
        v.right = remove(v.right, u.element);
      }

      setHeight(v);
      return balance(v);
    }

    int size() {
      return size;
    }
  }

  private Tree tree = new Tree();

  boolean contains(int x) {
    return tree.contains(x);
  }

  void insert(int x) {
    tree.root = tree.insert(tree.root, x);
  }

  void remove(int x) {
    tree.root = tree.remove(tree.root, x);
  }

  int size() {
    return tree.size();
  }
}
