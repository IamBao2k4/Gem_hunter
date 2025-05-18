import time
from pysat.formula import CNF
from pysat.solvers import Solver
from pysat.card import CardEnc
from itertools import product

class GemHunter:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        self.grid = [[cell.strip() for cell in line.split(',')] for line in lines]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0

        self.var_map = {}
        self.rev_map = {}
        vid = 1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '_':
                    self.var_map[(i, j)] = vid
                    self.rev_map[vid] = (i, j)
                    vid += 1
        self.num_vars = vid - 1

        self.number_cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j].isdigit():
                    num = int(self.grid[i][j])
                    neighbors = []
                    for dx, dy in product([-1, 0, 1], repeat=2):
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < self.rows and 0 <= nj < self.cols:
                            if self.grid[ni][nj] == '_' and (ni, nj) in self.var_map:
                                neighbors.append(self.var_map[(ni, nj)])
                    self.number_cells.append((num, neighbors))

    def solve_with_sat(self):
        start = time.time()
        cnf = CNF()

        for num, neighbors in self.number_cells:
            if len(neighbors) < num:
                print(f"Unsatisfiable: cell requires {num} traps but only has {len(neighbors)} neighbors")
                return None, 0.0, False
            if neighbors:
                cnf_enc = CardEnc.equals(lits=neighbors, bound=num, encoding=1)
                cnf.extend(cnf_enc.clauses)

        solver = Solver(bootstrap_with=cnf.clauses)
        success = solver.solve()
        grid_out = [row[:] for row in self.grid]

        if success:
            model = solver.get_model()
            assignment = {abs(v): v > 0 for v in model}
            for (i, j), var in self.var_map.items():
                grid_out[i][j] = 'T' if assignment.get(var, False) else 'G'

        solver.delete()
        end = time.time()
        return grid_out, end - start, success

    def solve_with_bruteforce(self):
        start = time.time()
        grid_out = [row[:] for row in self.grid]
        blanks = list(self.var_map.keys())
        V = len(blanks)

        solution = None
        for mask in range(1 << V):
            is_trap = {}
            for k in range(V):
                i, j = blanks[k]
                is_trap[(i, j)] = bool((mask >> k) & 1)
            ok = True
            for num, neigh_vars in self.number_cells:
                count = 0
                for var in neigh_vars:
                    i, j = self.rev_map[var]
                    if is_trap.get((i, j), False):
                        count += 1
                if count != num:
                    ok = False
                    break
            if ok:
                solution = is_trap
                break

        if solution:
            for (i, j), isT in solution.items():
                grid_out[i][j] = 'T' if isT else 'G'
        success = (solution is not None)
        end = time.time()
        return grid_out, end - start, success

    def solve_with_backtracking(self):
        start = time.time()
        grid_out = [row[:] for row in self.grid]
        blanks = list(self.var_map.keys())
        V = len(blanks)
        assign = [None] * V
        solution = None

        constraints = []
        for num, neigh_vars in self.number_cells:
            neigh_indices = []
            for idx, (i, j) in enumerate(blanks):
                if self.var_map[(i, j)] in neigh_vars:
                    neigh_indices.append(idx)
            constraints.append((num, neigh_indices))

        def backtrack(idx):
            nonlocal solution
            if solution is not None:
                return True
            if idx == V:
                solution = assign.copy()
                return True
            assign[idx] = False
            if self._check_partial(assign, constraints):
                if backtrack(idx + 1):
                    return True
            assign[idx] = True
            if self._check_partial(assign, constraints):
                if backtrack(idx + 1):
                    return True
            assign[idx] = None
            return False

        backtrack(0)
        if solution is not None:
            for k, (i, j) in enumerate(blanks):
                grid_out[i][j] = 'T' if solution[k] else 'G'
        success = (solution is not None)
        end = time.time()
        return grid_out, end - start, success

    def _check_partial(self, assign, constraints):
        for num, neigh in constraints:
            assigned_traps = 0
            unassigned = 0
            for idx in neigh:
                if assign[idx] is True:
                    assigned_traps += 1
                elif assign[idx] is None:
                    unassigned += 1
            if assigned_traps > num or assigned_traps + unassigned < num:
                return False
        return True

    def print_grid(self, grid):
        for row in grid:
            print(', '.join(row))

    def write_output(self, grid):
        out_name = self.filename.replace('input', 'output')
        with open(out_name, 'w') as f:
            for row in grid:
                f.write(', '.join(row) + '\n')
