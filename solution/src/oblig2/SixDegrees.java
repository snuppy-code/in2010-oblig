package oblig2;

import java.io.*;
import java.util.*;
import java.util.Queue;

public class SixDegrees {
    static abstract class Node {
        String id;
        ArrayList<Node> neighbors = new ArrayList<>();

        Node(String id) {
            this.id = id;
        }

        private void addNeighbor(Node e) {
            neighbors.add(e);
        }
    }

    static class Movie extends Node {
        String ttid;
        String title;
        double rating;

        Movie(String ttid, String title, double rating) {
            super(ttid);
            this.ttid = ttid;
            this.title = title;
            this.rating = rating;
        }
    }

    static class Actor extends Node {
        String nmid;
        String name;

        Actor(String nmid, String name) {
            super(nmid);
            this.nmid = nmid;
            this.name = name;
        }
    }

    static class Graf {
        HashMap<String, Node> nodes = new HashMap<>();

        void insertNode(Node n) {
            nodes.put(n.id, n);
        }

        void insertEdge(Node a, Node b) {
            a.addNeighbor(b);
            b.addNeighbor(a);
        }

        Node getNode(String id) {
            return nodes.get(id);
        }

        HashMap<Integer, Integer> finnSkuespillerKomponenter() {
            HashMap<Integer, Integer> components = new HashMap<>();
            HashSet<Node> visited = new HashSet<>();

            for (String k : nodes.keySet()) {
                Node n = nodes.get(k);

                if (!(n instanceof Actor && !visited.contains(n))) {
                    continue;
                }

                ArrayList<Node> component = new ArrayList<>();
                ArrayDeque<Node> q = new ArrayDeque<>();
                q.add(n);

                while (!(q.isEmpty())) {
                    Node u = q.remove();
                    visited.add(u);

                    if (u instanceof Actor) {
                        component.add(u);
                    }

                    for (Node v : u.neighbors) {
                        if (!(visited.contains(v))) {
                            visited.add(v);
                            q.add(v);
                        }
                    }
                }

                int componentSize = component.size();
                Integer componentAmount = components.get(componentSize);

                if (componentAmount == null) {
                    components.put(componentSize, 1);

                } else {
                    components.put(componentSize, componentAmount + 1);
                }
            }
            return components;
        }

        ArrayList<Node> finnKortesteVei(Actor a0, Actor a1) {
            ArrayList<Node> revPath = new ArrayList<>();

            if (a0 == a1) {
                revPath.add(a0);
                return revPath;
            }

            HashSet<Node> visited = new HashSet<>();
            ArrayDeque<Node> q = new ArrayDeque<>();
            HashMap<Node, Node> prev = new HashMap<>();

            q.add(a0);
            visited.add(a0);

            boolean pathFound = false;

            while (!(q.isEmpty())) {
                Node u = q.remove();

                if (u == a1) {
                    pathFound = true;
                    break;
                }

                for (Node v : u.neighbors) {
                    if (!(visited.contains(v))) {
                        prev.put(v, u);
                        visited.add(v);
                        q.add(v);
                    }
                }
            }

            if (!pathFound) {
                return null;
            }

            Node c = a1;

            while (!(c == null)) {
                revPath.add(c);
                c = prev.get(c);
            }

            Collections.reverse(revPath);
            return revPath;
        }

        static class QueueNode {
            Node node;
            double distance;

            QueueNode(Node node, double distance) {
                this.node = node;
                this.distance = distance;
            }
        }

        ArrayList<Node> finnChillesteVei(Actor a0, Actor a1) {
            ArrayList<Node> revPath = new ArrayList<>();
            if (a0 == a1) {revPath.add(a0); return revPath;}

            HashMap<Node, Double> dist = new HashMap<>();
            HashMap<Node, Node> prev = new HashMap<>();
            PriorityQueue<QueueNode> q = new PriorityQueue<>(Comparator.comparingDouble(e -> e.distance));

            for (String id : nodes.keySet()) {
                Node v = nodes.get(id);
                dist.put(v, Double.MAX_VALUE);
            }

            dist.put(a0, 0.0);
            q.add(new QueueNode(a0, 0.0));

            boolean pathFound = false;

            while (!(q.isEmpty())) {
                QueueNode qn = q.remove();
                Node v = qn.node;

                if (qn.distance > dist.get(v)) {
                    continue;
                }

                if (v == a1) {
                    pathFound = true;
                    break;
                }

                for (Node u : v.neighbors) {
                    double cost = 0;

                    if (u instanceof Movie m) {
                        cost = 10 - m.rating;
                    }

                    double newDist = dist.get(v) + cost;

                    if (newDist < dist.get(u)) {
                        prev.put(u, v);
                        dist.put(u, newDist);
                        q.add(new QueueNode(u, newDist));
                    }
                }
            }

            if (!pathFound) {
                return null;
            }

            Node c = a1;

            while (!(c == null)) {
                revPath.add(c);
                c = prev.get(c);
            }

            Collections.reverse(revPath);
            return revPath;
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));

        Graf grafen = new Graf();

        int M = Integer.parseInt(r.readLine());
        for (int i = 0; i < M; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [ttid, tittel, rating]
            grafen.insertNode(new Movie(parts[0], parts[1], Double.parseDouble(parts[2])));

        }

        int A = Integer.parseInt(r.readLine());
        for (int i = 0; i < A; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [id, navn]
            grafen.insertNode(new Actor(parts[0], parts[1]));
        }

        int E = Integer.parseInt(r.readLine());
        for (int i = 0; i < E; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [ttid, nmid]
            Node m = grafen.getNode(parts[0]);
            Node a = grafen.getNode(parts[1]);

            grafen.insertEdge(m, a);
        }

        HashMap<Integer, Integer> komponenter = grafen.finnSkuespillerKomponenter();
		System.out.println(komponenter.size()); // antall komponenter (bytt ut 0 med antall)

		for (Integer amount : komponenter.keySet()) {
		    System.out.println("There are " + komponenter.get(amount) + " components of size " + amount);
		}

        int Qs = Integer.parseInt(r.readLine());
        for (int i = 0; i < Qs; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [nmid₁, nmid₂]

			// Finn korteste vei
			// print på en linje

			Actor a0 = (Actor) grafen.getNode(parts[0]);
			Actor a1 = (Actor) grafen.getNode(parts[1]);

			ArrayList<Node> kortesteVei = grafen.finnKortesteVei(a0, a1);
			String s = "";

			for (Node v : kortesteVei) {
			    s = s + v.id + "\t";
			}

			System.out.println(s);
        }

        int Qc = Integer.parseInt(r.readLine());
        for (int i = 0; i < Qc; i++) {
            String[] parts = r.readLine().split("\t");
            // parts består av [nmid₁, nmid₂]

			// Finn korteste vei
			// print på en linje

			Actor a0 = (Actor) grafen.getNode(parts[0]);
			Actor a1 = (Actor) grafen.getNode(parts[1]);

			ArrayList<Node> chillesteVei = grafen.finnChillesteVei(a0, a1);
			String s = "";

			for (Node v : chillesteVei) {
			    s = s + v.id + "\t";
			}

			System.out.println(s);
        }
    }
}
