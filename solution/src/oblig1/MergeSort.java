package oblig1;

import java.io.BufferedReader;
import java.io.InputStreamReader;

class MergeSort {

    public static void main(String[] args) {
        // Read input
        BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
        int[] A = input.lines().mapToInt(i -> Integer.parseInt(i)).toArray();

        A = mergeSort(A);

        // Print result
        for (int num : A) {
            System.out.println(num);
        }
    }

    static int[] mergeSort(int[] A) {
        // Skriv her
        return A;
    }
}
