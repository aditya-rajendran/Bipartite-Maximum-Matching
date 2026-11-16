from collections import deque


def read_graph(filename):
    
    with open(filename, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    number_A, number_B = map(int, lines[0].split())

    # adjacency[a] contains the B-vertices connected to A-vertex a.
    adjacency = {a: [] for a in range(1, number_A + 1)}

    for line in lines[1:]:
        left_part, right_part = line.split(":", 1)
        a = int(left_part.strip())

        if right_part.strip():
            neighbours = list(map(int, right_part.split()))
        else:
            neighbours = []

        adjacency[a] = neighbours

    return number_A, number_B, adjacency


def construct_directed_graph(number_A, number_B, adjacency, matching):
    
    source = ("S", 0)
    sink = ("T", 0)

    directed_graph = {}

    def add_edge(start, end):
        if start not in directed_graph:
            directed_graph[start] = []
        directed_graph[start].append(end)

        # Make sure end also exists as a vertex in the graph.
        if end not in directed_graph:
            directed_graph[end] = []

    # Add the original graph edges with the required directions.
    for a in range(1, number_A + 1):
        for b in adjacency[a]:
            edge = (a, b)

            if edge in matching:
                # Matched edge: B -> A
                add_edge(("B", b), ("A", a))
            else:
                # Unmatched edge: A -> B
                add_edge(("A", a), ("B", b))

    matched_A = {a for a, b in matching}
    matched_B = {b for a, b in matching}

    # Source connects to all unmatched vertices in A.
    for a in range(1, number_A + 1):
        if a not in matched_A:
            add_edge(source, ("A", a))

    # All unmatched vertices in B connect to the sink.
    for b in range(1, number_B + 1):
        if b not in matched_B:
            add_edge(("B", b), sink)

    return directed_graph, source, sink


def find_augmenting_path(directed_graph, source, sink):
  
    queue = deque([source])#The queue is the list of vertices still waiting to be explored, and the source is first.
    parent = {source: None}

    while queue:
        current = queue.popleft()

        if current == sink:
            break

        for neighbour in directed_graph.get(current, []):
            if neighbour not in parent:
                parent[neighbour] = current
                queue.append(neighbour)

    # Sink was not reached: no augmenting path exists.
    if sink not in parent:
        return None

    # Reconstruct the path by following parent pointers backwards.
    path = []
    current = sink

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    # This is exactly Path \ {s, t} from the assignment.
    return path[1:-1]


def augment_matching(matching, augmenting_path):
  
    for i in range(len(augmenting_path) - 1):
        first = augmenting_path[i]
        second = augmenting_path[i + 1]

        # Convert the two typed vertices into the pair (A-vertex, B-vertex).
        if first[0] == "A":
            a = first[1]
            b = second[1]
        else:
            a = second[1]
            b = first[1]

        edge = (a, b)

        if edge in matching:
            matching.remove(edge)
        else:
            matching.add(edge)


def maximum_matching(number_A, number_B, adjacency):
   
    matching = set()

    while True:
        directed_graph, source, sink = construct_directed_graph(
            number_A, number_B, adjacency, matching
        )

        augmenting_path = find_augmenting_path(
            directed_graph, source, sink
        )

        if augmenting_path is None:
            break

        augment_matching(matching, augmenting_path)

    return matching


def main():
    filename = "Example1.g"  # Change this to "Example2.g" if needed.

    number_A, number_B, adjacency = read_graph(filename)

    matching = maximum_matching(number_A, number_B, adjacency)

    print("Maximum matching:")
    for a, b in sorted(matching):
        print(a, b)

    print("Matching size:", len(matching))


if __name__ == "__main__":
    main()
