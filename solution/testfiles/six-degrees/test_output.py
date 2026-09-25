import re
import traceback

def main(shortest_queries,
         chillest_queries,
         component_sizes,
         movies,
         actors,
         shortest_query_answers,
         chillest_query_answers):
    try:
        pattern = re.compile(r"\d+")

        sizes = frozenset({
            tuple(int(x.group()) for x in pattern.finditer(input()))
            for _ in range(int(input()))
        })

        if sizes != component_sizes:
            print("Wrong component count")
            print("    incorrect: ", set(sizes - component_sizes))
            print("    missing: ", set(component_sizes - sizes))

        graph = actors | movies

        errors = check_paths(graph, shortest_queries, shortest_query_answers, w=lambda _: 1)
        if errors:
            print("Errors in shortest path:")
            for error in errors:
                print("    " + error)

        errors = check_paths(graph, chillest_queries, chillest_query_answers, w=lambda id: 10-movies[id][1])
        if errors:
            print("Errors in chillest path:")
            for error in errors:
                print("    " + error)
    except EOFError:
        print("Not enough output")
    except Exception:
        print("Test program crashed")
        traceback.print_exc()
            
def normalize(id):
    return id[:2] + id[2:].lstrip("0")

def check_paths(graph, queries, answers, w):
    errors = []
    for query, answer in zip(queries, answers):
        path = [normalize(id) for id in input().split()]
        if not path:
            errors.append("Empty path")
            continue
        if {path[0], path[-1]} != set(query):
            errors.append("Path does not begin and end with the correct actors")
            continue

        for a, b in zip(path, path[1:]):
            if b not in graph[a][-1]:
                errors.append(f"Edge from {graph[a][0]} to {graph[b][0]} should not in a correct path.")

        if abs(answer - sum(w(id) for id in path[1::2])) > 0.01:
            errors.append(f"The path from {graph[path[0]][0]} to {graph[path[-1]][0]} is valid, but not optimal.")

    return errors
