
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    neighbors = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    visited = set()
    parent_dict = {}
    from_start_cost = {start: 0}
    total_cost = {start: heuristic(start, goal)}
    pq = []

    heapq.heappush(pq, (total_cost[start], start))

    while pq:
        current = heapq.heappop(pq)[1]

        if current == goal:
            path = []
            while current in parent_dict:
                path.append(current)
                current = parent_dict[current]
            path.reverse()
            return path

        visited.add(current)
        for i, j in neighbors:
            neighbor = (current[0] + i, current[1] + j)

            if not (0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]):
                continue
            if grid[neighbor[1], neighbor[0]] == 1:
                continue

            tentative_g_score = from_start_cost[current] + 1
            if neighbor in visited and tentative_g_score >= from_start_cost.get(neighbor, 0):
                continue

            if tentative_g_score < from_start_cost.get(neighbor, 0) or neighbor not in [n[1] for n in pq]:
                parent_dict[neighbor] = current
                from_start_cost[neighbor] = tentative_g_score
                total_cost[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(pq, (total_cost[neighbor], neighbor))

    return None
