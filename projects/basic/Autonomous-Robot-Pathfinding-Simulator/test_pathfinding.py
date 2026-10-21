
import unittest

from pathfinding_core import find_path


class TestPathfinding(unittest.TestCase):

    def setUp(self):
        self.start = (1, 1)
        self.goal = (5, 1)
        self.obstacles = {
            (3, y) for y in range(6)
        }
        self.grid_size = 7

    def test_known_shortest_route(self):
        path = find_path(
            self.start,
            self.goal,
            self.obstacles,
            self.grid_size
        )

        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.start)
        self.assertEqual(path[-1], self.goal)
        self.assertEqual(len(path) - 1, 14)

    def test_path_never_enters_obstacles(self):
        path = find_path(
            self.start,
            self.goal,
            self.obstacles,
            self.grid_size
        )

        self.assertIsNotNone(path)

        for position in path:
            self.assertNotIn(
                position, self.obstacles
            )

            x, y = position
            self.assertTrue(0 <= x < 7)
            self.assertTrue(0 <= y < 7)

        # Every move must be exactly one grid cell
        for a, b in zip(path, path[1:]):
            distance = (
                abs(a[0] - b[0])
                + abs(a[1] - b[1])
            )
            self.assertEqual(distance, 1)

    def test_no_available_path(self):
        full_wall = {
            (3, y) for y in range(7)
        }

        path = find_path(
            self.start,
            self.goal,
            full_wall,
            self.grid_size
        )

        self.assertIsNone(path)

    def test_start_equals_goal(self):
        path = find_path(
            (2, 2),
            (2, 2),
            set(),
            7
        )

        self.assertEqual(path, [(2, 2)])

    def test_invalid_goal(self):
        path = find_path(
            (1, 1),
            (9, 9),
            set(),
            7
        )

        self.assertIsNone(path)


if __name__ == "__main__":
    unittest.main()
