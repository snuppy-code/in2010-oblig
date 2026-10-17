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

	boolean contains(int x) {
		return false;
	}

	void insert(int x) {

	}

	void remove(int x) {

	}

	int size() {
		return 0;
	}
}
