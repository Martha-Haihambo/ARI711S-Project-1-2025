from collections import deque
from load import scientists, papers

def neighbors_for_scientist(scientist_id):
    neighbors = set()

    if scientist_id not in scientists:
        return neighbors

    for paper_id in scientists[scientist_id]["papers"]:
        for author_id in papers[paper_id]["authors"]:
            if author_id != scientist_id:  
                neighbors.add((paper_id, author_id))

    return neighbors

def shortest_path(source, target):
    if source not in scientists or target not in scientists:
        return None

    queue = deque([[(None, source)]])  
    visited = set([source])

    while queue:
        path = queue.popleft()
        last_paper, last_scientist = path[-1]

        if last_scientist == target:
            return path[1:]  

        for paper_id, neighbor in neighbors_for_scientist(last_scientist):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [(paper_id, neighbor)])

    return None  
