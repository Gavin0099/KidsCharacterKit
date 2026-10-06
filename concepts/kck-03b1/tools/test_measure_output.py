"""Verify the measurement helper's connectivity against an independent flood fill."""
from collections import deque
import unittest

import numpy as np
from measure_output import fill_holes, label4


class ComponentGeometry(unittest.TestCase):
    def test_random_topology_matches_flood_fill(self):
        rng = np.random.default_rng(42)
        for _ in range(100):
            mask = rng.random((12, 13)) > 0.5
            expected = []
            seen = set()
            for y, x in np.argwhere(mask):
                start = (int(y), int(x))
                if start in seen:
                    continue
                points = {start}
                seen.add(start)
                todo = deque([start])
                while todo:
                    yy, xx = todo.popleft()
                    for ny, nx in ((yy-1, xx), (yy+1, xx), (yy, xx-1), (yy, xx+1)):
                        p = (ny, nx)
                        if 0 <= ny < 12 and 0 <= nx < 13 and mask[p] and p not in seen:
                            seen.add(p)
                            points.add(p)
                            todo.append(p)
                expected.append(frozenset(points))
            labels, boxes = label4(mask)
            actual = [frozenset(map(tuple, np.argwhere(labels == i))) for i in range(1, len(boxes)+1)]
            self.assertEqual(set(expected), set(actual))
            for i, box in enumerate(boxes, 1):
                ys, xs = np.where(labels == i)
                self.assertEqual((box[0].start, box[0].stop, box[1].start, box[1].stop),
                                 (ys.min(), ys.max()+1, xs.min(), xs.max()+1))

    def test_holes_fill_but_open_regions_stay_open(self):
        closed = np.ones((5, 5), dtype=bool)
        closed[1:4, 1:4] = False
        self.assertTrue(fill_holes(closed).all())
        opened = closed.copy()
        opened[0, 2] = False
        np.testing.assert_array_equal(fill_holes(opened), opened)

    def test_empty_full_and_diagonal(self):
        for value, count in ((False, 0), (True, 1)):
            mask = np.full((3, 4), value)
            labels, boxes = label4(mask)
            self.assertEqual(len(boxes), count)
            np.testing.assert_array_equal(labels > 0, mask)
            np.testing.assert_array_equal(fill_holes(mask), mask)
        _, boxes = label4(np.eye(4, dtype=bool))
        self.assertEqual(len(boxes), 4)


if __name__ == "__main__":
    unittest.main()
