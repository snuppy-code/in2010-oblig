package oblig1;

import java.io.BufferedReader;
import java.io.InputStreamReader;

class InsertionSort {

    public static void main(String[] args) {
        // Read input
        BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
        int[] A = input.lines().mapToInt(i -> Integer.parseInt(i)).toArray();

        insertionSort(A);

        // Print result
        for (int num : A) {
            System.out.println(num);
        }
    }

    static void insertionSort(int[] A) {
        // Skriv her
    }
}
