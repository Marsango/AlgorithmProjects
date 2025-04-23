import numpy as np

def read_instance(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    n = int(lines[0])
    dist = np.zeros((n, n), dtype=int)
    for i in range(n):
        dist[i] = list(map(int, lines[1 + i].split()))
    time_windows = [tuple(map(int, line.split())) for line in lines[1 + n:]]
    return dist, time_windows

def greedy_tsp_with_tw_traveltime(dist, time_windows):
    n = len(dist)
    visited = [False] * n
    visited[0] = True
    path = [0]
    time = 0
    total_travel_time = 0

    while len(path) < n:
        current = path[-1]
        best_node = None
        best_arrival = float('inf')

        for next_node in range(1, n):  # ignora o depósito como destino
            if visited[next_node]:
                continue

            travel_time = dist[current][next_node]
            arrival_time = time + travel_time
            earliest, latest = time_windows[next_node]

            if arrival_time > latest:
                continue

            waiting_time = max(0, earliest - arrival_time)
            total_time = arrival_time + waiting_time

            if total_time < best_arrival:
                best_arrival = total_time
                best_node = next_node
                best_travel_time = travel_time

        if best_node is None:
            break

        visited[best_node] = True
        path.append(best_node)
        total_travel_time += best_travel_time
        time = best_arrival

    return path, total_travel_time

filename = 'n100w160.005.txt'
dist, tw = read_instance(filename)
path, cost = greedy_tsp_with_tw_traveltime(dist, tw)
print("Custo (travel time):", cost)
print("Permutação:", path)
