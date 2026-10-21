
from collections import deque


def find_path(start, goal, obstacles, grid_size):
    """Find a shortest path on a four-direction grid."""

    def valid(position):
        x, y = position

        return (
            0 <= x < grid_size
            and 0 <= y < grid_size
            and position not in obstacles
        )

    # Reject invalid starting or goal positions
    if not valid(start) or not valid(goal):
        return None

    queue = deque([start])
    previous = {start: None}

    directions = [
        (0, 1),    # Up
        (1, 0),    # Right
        (0, -1),   # Down
        (-1, 0)    # Left
    ]

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []

            while current is not None:
                path.append(current)
                current = previous[current]

            return list(reversed(path))

        for dx, dy in directions:
            neighbor = (
                current[0] + dx,
                current[1] + dy
            )

            if not valid(neighbor):
                continue

            if neighbor in previous:
                continue

            previous[neighbor] = current
            queue.append(neighbor)

    return None
