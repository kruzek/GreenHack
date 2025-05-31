import numpy as np
import heapq

def dijkstra(cost_matrix, start, goal):
    """
    Najkratšia cesta v 2D mriežke pomocou Dijkstra algoritmu (8 smerov).

    Args:
        cost_matrix (np.ndarray): 2D matica s nákladmi
        start (tuple): (row, col)
        goal (tuple): (row, col)

    Returns:
        list: Zoznam (row, col) bodov predstavujúcich cestu
    """
    rows, cols = cost_matrix.shape
    visited = np.full((rows, cols), False)
    dist = np.full((rows, cols), np.inf)
    prev = np.full((rows, cols, 2), -1, dtype=int)

    dist[start] = 0
    heap = [(0, start)]

    # 8 smerov (vrátane diagonál)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while heap:
        current_dist, (r, c) = heapq.heappop(heap)
        if visited[r, c]:
            continue
        visited[r, c] = True

        if (r, c) == goal:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                cost = cost_matrix[nr, nc]
                if cost == np.inf:
                    continue
                # Diagonály sú drahšie
                factor = np.sqrt(2) if dr != 0 and dc != 0 else 1
                new_dist = current_dist + cost * factor
                if new_dist < dist[nr, nc]:
                    dist[nr, nc] = new_dist
                    prev[nr, nc] = [r, c]
                    heapq.heappush(heap, (new_dist, (nr, nc)))

    # Rekonštrukcia cesty
    path = []
    r, c = goal
    if dist[r, c] == np.inf:
        return []  # Nedostupné

    while (r, c) != start:
        path.append((r, c))
        r, c = prev[r, c]
    path.append(start)
    path.reverse()
    return path

def dijkstra_and_save_txt(cost_matrix, start, goal, txt_path="shortest_path.txt"):
    """
    Spustí Dijkstra algoritmus a uloží výslednú cestu do .txt.

    Returns:
        path (list): Zoznam súradníc [(row, col), ...]
    """
    path = dijkstra(cost_matrix, start, goal)
    if path:
        with open(txt_path, "w") as f:
            for row, col in path:
                f.write(f"{row},{col}\n")
    return path
