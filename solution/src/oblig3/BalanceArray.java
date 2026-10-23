package oblig3;

import java.io.*;

class BalanceArray {

    static void printBalanced(int[] array) {
        printBalanced(array, 0, array.length - 1);
    }

    static void printBalanced(int[] array, int low, int high) {
        if (low > high) {
            return;
        }

        int mid = low + (high - low) / 2;
        System.out.println(array[mid]);

        printBalanced(array, low, mid - 1);
        printBalanced(array, mid + 1, high);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        int[] array = in
            .lines()
            .mapToInt(i -> Integer.parseInt(i))
            .toArray();
        printBalanced(array);
    }
}
