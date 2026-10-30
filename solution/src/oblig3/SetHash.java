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

    private static final double MAX_LOAD_FACTOR = 1;
    private InternalArray array = new InternalArray(16);

    private void rehash(int newCapacity) {
        InternalArray na = new InternalArray(newCapacity);

        for (InternalArray.Node e : array.entries) {
            InternalArray.Node curr = e;

            while (curr != null) {
                na.insertNew(curr.v);
                curr = curr.next;
            }
        }

        array = na;
    }

    private static class InternalArray {

        private int size = 0;
        private Node[] entries;

        InternalArray(int capacity) {
            this.entries = new Node[capacity];
        }

        private int hash(int v) {
            return Math.floorMod(v, entries.length);
        }

        public boolean contains(int x) {
            Node curr = entries[hash(x)];
            while (curr != null) {
                if (curr.v == x) {
                    return true;
                }
                curr = curr.next;
            }
            return false;
        }

        public void insert(int x) {
            if (contains(x)) {
                return;
            }
            insertNew(x);
        }

        private void insertNew(int x) {
            int i = hash(x);
            entries[i] = new Node(x, entries[i]);
            size++;
        }

        public void remove(int x) {
            int i = hash(x);

            Node prev = null;
            Node curr = entries[i];

            while (curr != null) {
                if (curr.v == x) {
                    if (prev != null) {
                        prev.next = curr.next;
                    } else {
                        entries[i] = curr.next;
                    }
                    size--;
                    return;
                }
                prev = curr;
                curr = curr.next;
            }
        }

        public int size() {
            return size;
        }

        private static class Node {

            int v;
            Node next;

            Node(int v, Node next) {
                this.v = v;
                this.next = next;
            }
        }
    }

    boolean contains(int x) {
        return array.contains(x);
    }

    void insert(int x) {
        array.insert(x);
        if ((double) array.size() / array.entries.length >= MAX_LOAD_FACTOR) {
            rehash(array.entries.length * 2);
        }
    }

    void remove(int x) {
        array.remove(x);
    }

    int size() {
        return array.size();
    }
}
