from main import read_instance, greedy_tsp_with_tw_traveltime


def evaluate_path(dist, time_windows, path):
    time = 0
    total_travel = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        travel_time = dist[u][v]
        arrival = time + travel_time
        earliest, latest = time_windows[v]
        if arrival > latest:
            return None, float('inf')  # infeasible
        wait = max(0, earliest - arrival)
        time = arrival + wait
        total_travel += travel_time
    return time, total_travel

def two_opt_with_tw(dist, time_windows, initial_path):
    best_path = initial_path.copy()
    _, best_cost = evaluate_path(dist, time_windows, best_path)
    improved = True

    while improved:
        improved = False
        n = len(best_path)
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                new_path = best_path[:i] + best_path[i:j + 1][::-1] + best_path[j + 1:]
                end_time, cost = evaluate_path(dist, time_windows, new_path)
                if cost < best_cost:
                    best_path = new_path
                    best_cost = cost
                    improved = True
                    break
            if improved:
                break
    return best_path, best_cost


if __name__ == '__main__':
    filename = 'instances/n100w160.005.txt'
    dist, tw = read_instance(filename)
    path, cost = greedy_tsp_with_tw_traveltime(dist, tw)
    improved_path, improved_cost = two_opt_with_tw(dist, tw, path)
    print("Custo (travel time) | GULOSO:", cost)
    print("Permutação | GULOSO:", path)
    print("Custo (travel time) | 2  OPT:", improved_cost)
    print("Permutação | 2 OPT:", improved_path)