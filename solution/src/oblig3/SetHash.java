package oblig3;

import java.io.*;

class SetHash {
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int N = Integer.parseInt(br.readLine());
    SetHash set = new SetHash();

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

  private InternalArray array = new InternalArray(16);

  private void rehash(int newCapacity) {
    InternalArray newArray = new InternalArray(newCapacity);

    for (InternalArray.ArrayEntry e : array.entries) {
      if (e != null && e.v != null) {
        newArray.insertWithoutResize(e.v);
      }
    }

    array = newArray;
  }

  boolean contains(int x) {
    return array.contains(x);
  }

  void insert(int x) {
    array.insert(x);
  }

  void remove(int x) {
    array.remove(x);
  }

  int size() {
    return array.size();
  }

  private class InternalArray {
    private static final double MAX_LOAD_FACTOR = 0.625;

    int capacity;
    int size = 0;
    int deletedElements = 0;
    ArrayEntry[] entries;

    InternalArray(int capacity) {
      this.capacity = capacity;
      this.entries = new ArrayEntry[capacity];
    }

    int hash(int v) {
      return Math.floorMod(v, capacity);
    }

    void resize() {
      if ((double) (size + deletedElements) / capacity >= MAX_LOAD_FACTOR) {
        if ((double) size / capacity >= MAX_LOAD_FACTOR * 0.8) {
          rehash(capacity * 2);
        } else {
          rehash(capacity);
        }
      }
    }

    boolean contains(int x) {
      int start = hash(x);
      int i = start;

      do {
        ArrayEntry entry = entries[i];

        if (entry == null) {
          return false;

        } else if (entry.v != null && entry.v == x) {
          return true;
        }

        i++;

        if (i == capacity) {
          i = 0;
        }

      } while (i != start);

      return false;
    }

    void insert(int x) {
      if (contains(x)) {
        return;
      }

      insertWithoutResize(x);
      resize();
    }

    void insertWithoutResize(int x) {
      int start = hash(x);
      int i = start;

      do {
        ArrayEntry entry = entries[i];

        if (entry == null || entry.v == null) {
          if (entry != null) {
            deletedElements--;
          }

          entries[i] = new ArrayEntry(x);
          size++;
          break;
        }

        i++;

        if (i == capacity) {
          i = 0;
        }

      } while (i != start);
    }

    void remove(int x) {
      int start = hash(x);
      int i = start;

      do {
        ArrayEntry entry = entries[i];

        if (entry == null) {
          return;

        } else if (entry.v != null && entry.v == x) {
          entry.v = null;
          deletedElements++;
          size--;
          return;
        }

        i++;

        if (i == capacity) {
          i = 0;
        }

      } while (i != start);
    }

    int size() {
      return size;
    }

    private static class ArrayEntry {
      Integer v = null;

      ArrayEntry(Integer v) {
        this.v = v;
      }
    }
  }
}
