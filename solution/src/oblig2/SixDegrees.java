package oblig2;

import java.io.*;
import java.util.*;

class SixDegrees {
    public static void main(String[] args) throws Exception {
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));

        System.err.println("Dette er et eksempel på å printe debug info. Du kan slette denne linjen");

        int M = Integer.parseInt(r.readLine());
        for (int i = 0; i < M; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [ttid, tittel, rating]
        }

        int A = Integer.parseInt(r.readLine());
        for (int i = 0; i < A; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [id, navn]
        }

        int E = Integer.parseInt(r.readLine());
        for (int i = 0; i < E; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [ttid, nmid]
        }

		// Finn antall komponenter
		System.out.println(0); // antall komponenter (bytt ut 0 med antall)


        int Qs = Integer.parseInt(r.readLine());
        for (int i = 0; i < Qs; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [nmid₁, nmid₂]

			// Finn korteste vei
			// print på en linje
        }

        int Qc = Integer.parseInt(r.readLine());
        for (int i = 0; i < Qc; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [nmid₁, nmid₂]

			// Finn korteste vei
			// print på en linje
        }
    }
}

