import os
import csv
import numpy as np

def read_instance(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
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

        for next_node in range(1, n):
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

if __name__ == '__main__':
    from twoopt import two_opt_with_tw
    folder = 'instances'
    results = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):

            dist, tw = read_instance(filepath)
            path_greedy, cost_greedy = greedy_tsp_with_tw_traveltime(dist, tw)
            path_2opt, cost_2opt = two_opt_with_tw(dist, tw, path_greedy)
            results.append((filename, cost_greedy, cost_2opt))

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file', 'cost_greedy', 'cost_2opt'])
        writer.writerows(results)