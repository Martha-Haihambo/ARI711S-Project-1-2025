import sys

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        self.domains = {
            (i, j): [board[i][j]] if board[i][j] != 0 else list(range(1, 10))
            for i in range(9) for j in range(9)
        }


    def get_peers(self, cell):
        i, j = cell
        peers = set()
        for x in range(9):
            if x != j:
                peers.add((i, x))
            if x != i:
                peers.add((x, j))
        box_row = (i // 3) * 3
        box_col = (j // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (i, j):
                    peers.add((r, c))
        return peers



    def enforce_node_consistency(self):
        for cell in self.variables:
            if len(self.domains[cell]) == 1:
                value = self.domains[cell][0]
                for peer in self.get_peers(cell):
                    if value in self.domains[peer] and len(self.domains[peer]) > 1:
                        self.domains[peer].remove(value)



    def revise(self, x, y):
        revised = False
        to_remove = []
        for val in self.domains[x]:
            if all(val == other_val for other_val in self.domains[y]):
                to_remove.append(val)
        if to_remove:
            for val in to_remove:
                self.domains[x].remove(val)
            revised = True
        return revised
    


    def ac3(self):
        queue = [(x, y) for x in self.variables for y in self.get_peers(x)]
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.get_peers(x):
                    if z != y:
                        queue.append((z, x))
        return True



    def assignment_complete(self, assignment):
        return all(len(assignment[v]) == 1 for v in self.variables)



    def consistent(self, assignment):
        for cell in self.variables:
            if len(assignment[cell]) == 1:
                val = assignment[cell][0]
                for peer in self.get_peers(cell):
                    if len(assignment[peer]) == 1 and assignment[peer][0] == val:
                        return False
        return True



    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.variables if len(assignment[v]) > 1]
        if not unassigned:
            return None
        min_domain = min(len(assignment[v]) for v in unassigned)
        candidates = [v for v in unassigned if len(assignment[v]) == min_domain]
        return max(candidates, key=lambda v: len(self.get_peers(v)))



    def order_domain_values(self, var, assignment):
        def count_conflicts(value):
            return sum(value in assignment[peer] for peer in self.get_peers(var))
        return sorted(assignment[var], key=count_conflicts)



    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        if var is None:
            return None
        for value in self.order_domain_values(var, assignment):
            new_assignment = {v: list(assignment[v]) for v in assignment}
            new_assignment[var] = [value]
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
        return None



    def solve(self):
        self.enforce_node_consistency()
        if not self.ac3():
            return None
        result = self.backtrack(self.domains)
        if result:
            self.board = [[result[(i, j)][0] for j in range(9)] for i in range(9)]
            return self.board
        else:
            return None



def load_puzzle_from_file(filename):
    puzzle = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                puzzle.append([int(char) for char in line if char.isdigit()])
    return puzzle



def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("+-------+-------+-------+")
        for j in range(9):
            if j % 3 == 0:
                print("| ", end="")
            print(board[i][j], end=" ")
            if j == 8:
                print("|")
    print()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sudoku_solver.py <puzzle_file>")
        sys.exit(1)
    try:
        puzzle = load_puzzle_from_file(sys.argv[1])
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    solver = SudokuSolver(puzzle)
    solution = solver.solve()

    if solution:
        print("\nSolved Sudoku:\n")
        print_board(solution)
    else:
        print("No solution found.")

