# Maximum Matching in a Bipartite Graph

Finds a maximum matching in a bipartite graph with the augmenting-path algorithm. The program reads a graph from a `.g` file, grows a matching until no augmenting path remains, and prints the matched edges.

It uses only the Python standard library (`collections.deque`).

## Algorithm

The matching starts empty. Each round does three things:

1. Build a directed graph from the current matching.
   - Unmatched edges point from A to B.
   - Matched edges point from B to A.
   - A source points at every free A-vertex.
   - Every free B-vertex points at a sink.
2. Search for a path from the source to the sink with breadth-first search.
3. Flip the edges on that path: unmatched edges become matched, and matched edges become unmatched.

The search returns no path once the matching is maximum. Each successful round increases the matching by one edge.

## Run

Requires Python 3.

Set the input file in `main()` inside `augmenting_path_matching.py`:

```python
filename = "Example1.g"
```

Then run:

```bash
python augmenting_path_matching.py
```

`Example1.g` prints:

```text
Maximum matching:
1 3
2 1
3 2
Matching size: 3
```

Each line `a b` means A-vertex `a` is matched to B-vertex `b`.

## Input format

The first line is the number of vertices on side A and side B. Each following line lists the neighbours in B of one A-vertex. Vertices are numbered from 1. A line with nothing after the colon means that A-vertex has no edges.

`Example1.g`:

```text
3 3
1: 1 2 3
2: 1
3: 2
```

A-vertex 1 is connected to B-vertices 1, 2, and 3. A-vertex 2 is connected only to B-vertex 1. A-vertex 3 is connected only to B-vertex 2.

## Sample files

| File | Matching size |
| --- | --- |
| `Example1.g` | 3 |
| `Example2.g` | 4 |
| `Test1.g` | 8 |
| `Test2.g` | 3 |
| `Test3.g` | 5 |

## Files

- `augmenting_path_matching.py` reads a graph and computes a maximum matching.
- `Example1.g`, `Example2.g`, `Test1.g`, `Test2.g`, `Test3.g` are sample graphs.
