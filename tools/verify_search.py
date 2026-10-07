"""Reproduce Homework 1 results with A* and independent BFS (standard library)."""
from collections import deque
from heapq import heappop, heappush
from itertools import count
import json

SQUARES = 'A3 A4 A5 B1 B2 B3 B5 C3 C5 D3 D4 D5'.split()
ACCESSIBLE = set(SQUARES)
FRIENDS = {'A3': 1, 'D3': 2}


def xy(square):
    return ord(square[0]) - ord('A') + 1, int(square[1])


def manhattan(a, b):
    x, y = xy(a)
    u, v = xy(b)
    return abs(x - u) + abs(y - v)


def neighbors(square):
    x, y = xy(square)
    for dx, dy in [(0, 1), (-1, 0), (1, 0)]:  # Up, Left, Right
        candidate = chr(ord('A') + x + dx - 1) + str(y + dy)
        if candidate in ACCESSIBLE:
            yield candidate


def astar(start, goal):
    serial = count()
    heap = [(manhattan(start, goal), manhattan(start, goal), next(serial), 0, start)]
    best = {start: 0}
    parent = {start: None}
    closed = set()
    popped, generated = [], []
    while heap:
        f, h, _, g, square = heappop(heap)
        if square in closed or g != best[square]:
            continue
        popped.append({'square': square, 'triple': [f, g, h]})
        if square == goal:
            path = []
            while square is not None:
                path.append(square)
                square = parent[square]
            return {'cost': g, 'path': path[::-1], 'popped': popped, 'generated': generated}
        closed.add(square)
        for nxt in neighbors(square):
            ng, nh = g + 1, manhattan(nxt, goal)
            accepted = ng < best.get(nxt, float('inf'))
            generated.append({'from': square, 'to': nxt, 'triple': [ng + nh, ng, nh], 'accepted': accepted})
            if accepted:
                best[nxt], parent[nxt] = ng, square
                heappush(heap, (ng + nh, nh, next(serial), ng, nxt))
    raise ValueError(f'Unreachable: {start} -> {goal}')


def bfs_full_state():
    start = ('B1', 0)
    queue = deque([start])
    distance, parent = {start: 0}, {start: None}
    while queue:
        state = queue.popleft()
        square, mask = state
        if state == ('C5', 3):
            path = []
            cursor = state
            while cursor is not None:
                path.append(list(cursor))
                cursor = parent[cursor]
            return {'cost': distance[state], 'states': path[::-1]}
        for nxt in neighbors(square):
            new_state = (nxt, mask | FRIENDS.get(nxt, 0))
            if new_state not in distance:
                distance[new_state] = distance[state] + 1
                parent[new_state] = state
                queue.append(new_state)
    raise ValueError('No solution')


def main():
    stages = [astar('B1', 'A3'), astar('A3', 'D3'), astar('D3', 'C5')]
    alternate = [astar('B1', 'D3'), astar('D3', 'A3'), astar('A3', 'C5')]
    path = stages[0]['path'] + stages[1]['path'][1:] + stages[2]['path'][1:]
    bfs = bfs_full_state()
    assert path == 'B1 B2 B3 A3 B3 C3 D3 D4 D5 C5'.split()
    assert all(b in set(neighbors(a)) for a, b in zip(path, path[1:]))
    assert sum(s['cost'] for s in stages) == bfs['cost'] == 9
    assert sum(s['cost'] for s in alternate) == 11
    assert path.index('A3') < path.index('C5') and path.index('D3') < path.index('C5')
    for goal in ['A3', 'D3', 'C5']:
        assert manhattan(goal, goal) == 0
        for a in SQUARES:
            for b in neighbors(a):
                assert manhattan(a, goal) <= 1 + manhattan(b, goal)
    result = {
        'columns': SQUARES,
        'manhattan': {goal: [manhattan(s, goal) for s in SQUARES] for goal in ['A3', 'D3', 'C5']},
        'stages': stages,
        'alternate_order_cost': sum(s['cost'] for s in alternate),
        'optimal_path': path,
        'optimal_cost': len(path) - 1,
        'independent_bfs': bfs,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
