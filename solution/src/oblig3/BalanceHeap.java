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
    }
}
