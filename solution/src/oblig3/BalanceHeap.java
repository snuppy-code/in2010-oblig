package oblig3;

import java.io.*;
import java.util.PriorityQueue;

class BalanceHeap {

  public static void main(String[] args) throws IOException {
    PriorityQueue<Integer> heap = new PriorityQueue<Integer>();
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    for (String line = in.readLine(); line != null; line = in.readLine()) {
      heap.offer(Integer.parseInt(line));
    }
    printBalanced(heap);
  }

  static void printBalanced(PriorityQueue<Integer> heap) {
    int size = heap.size();

    if (size == 1) {
      Integer p = heap.poll();
      System.out.println(p);
      return;
    }

    if (size < 1) {
      return;
    }

    PriorityQueue<Integer> left = new PriorityQueue<>();
    PriorityQueue<Integer> right = new PriorityQueue<>();

    for (int i = 0; i < size / 2; i++) {
      Integer p = heap.poll();
      left.add(p);
    }

    System.out.println(heap.poll());

    for (int i = size / 2 + 1; i < size; i++) {
      Integer p = heap.poll();
      right.add(p);
    }

    printBalanced(left);
    printBalanced(right);
  }
}
