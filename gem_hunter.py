import time
from itertools import product, combinations
from pysat.formula import CNF
from pysat.solvers import Glucose3

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
                    self.number_cells.append((num, neighbors, i, j))

        self.validate_input()

    def validate_input(self):
        for num, neighbors, i, j in self.number_cells:
            if len(neighbors) < num:
                print(f"[INVALID INPUT] Cell at ({i},{j}) requires {num} traps but only has {len(neighbors)} empty neighbors.")

    def solve_with_sat(self):
        start_time = time.time()
        clauses = []

        for num, neighbors, i, j in self.number_cells:
            if len(neighbors) < num:
                print(f"Unsatisfiable at ({i}, {j}): cell requires {num} traps but only has {len(neighbors)} neighbors")
                return None, 0.0, False
            if neighbors:
                clauses += self.encode_exactly_k(neighbors, num)

        cnf = CNF()
        cnf.extend(clauses)

        solver = Glucose3()
        solver.append_formula(cnf)

        success = solver.solve()
        grid_out = [row[:] for row in self.grid]

        if success:
            model = solver.get_model()
            assignment = {abs(v): v > 0 for v in model}
            for (i, j), var in self.var_map.items():
                grid_out[i][j] = 'T' if assignment.get(var, False) else 'G'

        solver.delete()
        end_time = time.time()

        return grid_out, end_time - start_time, success

    def encode_exactly_k(self, var_ids, k):
        clauses = []
        if k > 0:
            for combo in combinations(var_ids, len(var_ids) - k + 1):
                clauses.append(list(combo))
        if k < len(var_ids):
            for combo in combinations(var_ids, k + 1):
                clauses.append([-v for v in combo])
        return clauses

    def solve_with_bruteforce(self):
        start = time.time()
        grid_out = [row[:] for row in self.grid]
        blanks = list(self.var_map.keys())
        V = len(blanks)

        solution = None
        if V < 20:
            for mask in range(1 << V):
                is_trap = {}
                for k in range(V):
                    i, j = blanks[k]
                    is_trap[(i, j)] = bool((mask >> k) & 1)
                ok = True
                for num, neigh_vars, _, _ in self.number_cells:
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
        else:
            print("Grid too large for brute-force search.")
            return grid_out, 0.0, False
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
        model = [None] * (self.rows * self.cols + 1)
        solution_found = [False]

        constraints = []
        for num, neigh_vars, _, _ in self.number_cells:
            indices = []
            for (i, j) in blanks:
                var = self.var_map[(i, j)]
                if var in neigh_vars:
                    indices.append(var)
            constraints.append((num, indices))

        def check_constraints(model):
            for num, neigh_vars in constraints:
                count_true = 0
                count_undef = 0
                for var in neigh_vars:
                    if model[var] is True:
                        count_true += 1
                    elif model[var] is None:
                        count_undef += 1
                if count_true > num or count_true + count_undef < num:
                    return False
            return True

        def backtrack(index):
            if index == len(blanks):
                solution_found[0] = True
                return True

            i, j = blanks[index]
            var = self.var_map[(i, j)]

            for value in [True, False]:
                model[var] = value
                if check_constraints(model):
                    if backtrack(index + 1):
                        return True
                model[var] = None

            return False

        backtrack(0)
        if solution_found[0]:
            for (i, j), var in self.var_map.items():
                grid_out[i][j] = 'T' if model[var] else 'G'
        success = solution_found[0]
        end = time.time()
        return grid_out, end - start, success

    def print_grid(self, grid):
        for row in grid:
            print(', '.join(row))

    def write_output(self, grid, method_name):
        out_name = self.filename.replace('input', 'output' + method_name)
        with open(out_name, 'w') as f:
            for row in grid:
                f.write(', '.join(row) + '\n')
