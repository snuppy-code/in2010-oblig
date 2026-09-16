// Implementert både i python og java.
// De burde være ganske like.
// Gi gjerne tilbakemelding på begge :)

package oblig1;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

class MergeSort {
    private static int[] merge(int[] A1, int[] A2, int[] A) {
        int i = 0;
        int j = 0;

        while (i < A1.length && j < A2.length) {
            if (A1[i] > A2[j]) {
                A[i + j] = A2[j];
                j++;

            } else {
                A[i + j] = A1[i];
                i++;
            }
        }

        while (i < A1.length) {
            A[i + j] = A1[i];
            i++;
        }

        while (j < A2.length) {
            A[i + j] = A2[j];
            j++;
        }

        return A;
    }

    public static int[] mergeSort(int[] A) {
        if (A.length <= 1) {
            return A;
        }

        int[] l = mergeSort(Arrays.copyOfRange(A, 0, (int) A.length / 2));
        int[] r = mergeSort(Arrays.copyOfRange(A, (int) A.length / 2, A.length));

        return merge(l, r, A);
    }

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
}
