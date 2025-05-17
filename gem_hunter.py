import numpy as np
from typing import List, Tuple, Set
import time
from pysat.solvers import Glucose3
from pysat.formula import CNF
from itertools import combinations

class GemHunter:
    def __init__(self, grid_size: Tuple[int, int], numbered_cells: List[Tuple[int, int, int]]):
        self.rows, self.cols = grid_size
        self.grid = np.zeros(grid_size, dtype=int)
        self.numbered_cells = numbered_cells
        
        # Initialize grid with numbered cells
        for row, col, num in numbered_cells:
            self.grid[row, col] = num
            
        # Create variable mapping for CNF
        self.var_mapping = {}
        self.reverse_mapping = {}
        self._create_variable_mapping()

    def is_numbered_cell(self, row: int, col: int) -> bool:
        for r, c, _ in self.numbered_cells:
            if (row, col) == (r, c):
                return True
        
    def _create_variable_mapping(self):
        var_id = 1
        for i in range(self.rows):
            for j in range(self.cols):
                self.var_mapping[(i, j)] = var_id
                self.reverse_mapping[var_id] = (i, j)
                var_id += 1
                
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neightbors_pos = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1),
                          (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)]
        
        neightbors = []

        for r, c in neightbors_pos:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neightbors.append((r, c))

        return neightbors
    
    def generate_cnf(self) -> CNF:
        cnf = CNF()
        
        # First, add constraints to ensure numbered cells cannot be traps
        for row, col, _ in self.numbered_cells:
            var_id = self.var_mapping[(row, col)]
            cnf.append([-var_id])  # Force numbered cells to not be traps
        
        # For each numbered cell, create constraints for exactly num traps
        for row, col, num in self.numbered_cells:
            neighbors = self.get_neighbors(row, col)
            # Filter out numbered cells from neighbors
            valid_neighbors = []
            for n_row, n_col in neighbors:
                if not self.is_numbered_cell(n_row, n_col):
                    valid_neighbors.append((n_row, n_col))
            neighbor_vars = [self.var_mapping[n] for n in valid_neighbors]
            
            # "At least num" - Every combination of (len(neighbors) - num + 1) cells must contain at least one trap if num > 0
            if num > 0 and len(neighbor_vars) > num:
                for subset in combinations(neighbor_vars, len(neighbor_vars) - num + 1):
                    cnf.append([v for v in subset])
            
            # "At most num" - Every combination of (num + 1) cells must contains number of gem = len(neighbors_vars) - num
            if num < len(neighbor_vars):
                for subset in combinations(neighbor_vars, num + 1):
                    cnf.append([-v for v in subset])
        return cnf
        
    def solve_with_pysat(self) -> Tuple[bool, List[int], float]:
        cnf = self.generate_cnf()   
        solver = Glucose3()
        solver.append_formula(cnf)
        
        start_time = time.time()
        satisfiable = solver.solve()
        end_time = time.time()
        
        if satisfiable:
            model = solver.get_model()
            
            # Initialize all cells as gems (-1)
            assignment = [-1] * (self.rows * self.cols)
            
            # Set traps based on positive variables in the model
            for var in model:
                if var > 0 and var <= len(assignment):
                    var_id = var
                    row, col = self.reverse_mapping[var_id]
                    pos = row * self.cols + col
                    assignment[pos] = 1  # This is a trap
            
            # Ensure numbered cells are set correctly (they should be neither trap nor gem)
            for row, col, _ in self.numbered_cells:
                pos = row * self.cols + col
                assignment[pos] = 0  # Mark as numbered cell
            
            return True, assignment, end_time - start_time
        
        # If unsatisfiable, print more info
        print("SAT solver found problem unsatisfiable")
        return False, None, end_time - start_time
    
    def solve_brute_force(self) -> Tuple[bool, List[int], float]:
        start_time = time.time()
        n_vars = self.rows * self.cols
        numbered_positions = set((row * self.cols + col) for row, col, _ in self.numbered_cells)
        non_numbered_positions = [i for i in range(n_vars) if i not in numbered_positions]
        n_non_numbered = len(non_numbered_positions)

        # Precompute valid bounds for each numbered cell
        constraints = {pos: num for row, col, num in self.numbered_cells for pos in [row * self.cols + col]}

        def _is_valid_assignment(assignment: List[int], constraints: dict) -> bool:
            for pos, num in constraints.items():
                row, col = pos // self.cols, pos % self.cols
                neighbors = self.get_neighbors(row, col)
                trap_count = sum(1 for n in neighbors if assignment[n[0] * self.cols + n[1]] == 1)
                
                if trap_count != num:
                    return False
            return True

        # Try all possible combinations for non-numbered cells using bit manipulation
        for mask in range(1 << n_non_numbered):  
            assignment = [0] * n_vars  # 0 for numbered cells
            for idx, pos in enumerate(non_numbered_positions):
                assignment[pos] = 1 if (mask >> idx) & 1 else -1  # Use bit manipulation to assign trap/gem

            # Check constraints early to prune invalid cases
            if _is_valid_assignment(assignment, constraints):
                end_time = time.time()
                return True, assignment, end_time - start_time

        end_time = time.time()
        return False, None, end_time - start_time
    
    def _is_valid_assignment(self, assignment: List[int]) -> bool:
        for row, col, num in self.numbered_cells:
            neighbors = self.get_neighbors(row, col)
            trap_count = sum(1 for n in neighbors if assignment[self.var_mapping[n]-1] > 0)
            if trap_count != num:
                return False
        return True
    
    def solve_backtracking(self) -> Tuple[bool, List[int], float]:
        start_time = time.time()
        n_vars = self.rows * self.cols
        assignment = [0] * n_vars
        
        def check_constraints(pos: int) -> bool:
            # Check all numbered cells
            for row, col, num in self.numbered_cells:
                neighbors = self.get_neighbors(row, col)
                trap_count = 0
                assigned_count = 0
                
                # Count traps and assigned cells in neighbors
                for n_row, n_col in neighbors:
                    n_pos = n_row * self.cols + n_col
                    if n_pos <= pos and assignment[n_pos] != 0:  # Only check assigned positions
                        assigned_count += 1
                        if assignment[n_pos] > 0:  # If it's a trap
                            trap_count += 1
                
                # If we have too many traps already, this is invalid
                if trap_count > num:
                    return False
                
                # If all neighbors are assigned, we must have exactly num traps
                if assigned_count == len(neighbors) and trap_count != num:
                    return False
                
                # If some neighbors are unassigned, check if we can still satisfy the constraint
                if assigned_count < len(neighbors):
                    remaining_cells = len(neighbors) - assigned_count
                    # We need at least (num - trap_count) more traps
                    min_required_traps = num - trap_count
                    # We can't have more traps than remaining cells
                    if min_required_traps > remaining_cells:
                        return False
                    # We can't have more traps than the number requires
                    if trap_count + remaining_cells < num:
                        return False
            
            return True

        def backtrack(pos: int) -> bool:
            if pos == n_vars:
                return True  # All positions assigned and constraints satisfied
            
            row, col = pos // self.cols, pos % self.cols
            # Skip numbered cells as they can't be traps or gems
            if self.is_numbered_cell(row, col):
                assignment[pos] = 0  # Just to be explicit
                return backtrack(pos + 1)

            # Try setting current position to trap
            assignment[pos] = 1
            if check_constraints(pos) and backtrack(pos + 1):
                return True
                
            # Try setting current position to gem
            assignment[pos] = -1
            if check_constraints(pos) and backtrack(pos + 1):
                return True
                
            # Backtrack
            assignment[pos] = 0
            return False
        
        solution_found = backtrack(0)
        end_time = time.time()
        
        if solution_found:
            return True, assignment, end_time - start_time
        return False, None, end_time - start_time
        
    def display_solution(self, solution: List[int]):
        if not solution:
            print("No solution found!")
            return
            
        display_grid = np.zeros((self.rows, self.cols), dtype=str)
        for i in range(self.rows):
            for j in range(self.cols):
                var_id = self.var_mapping[(i, j)]
                if solution[var_id-1] > 0:
                    display_grid[i, j] = 'T'  # Trap
                else:
                    display_grid[i, j] = 'G'  # Gem
                    
        # Overlay numbered cells
        for row, col, num in self.numbered_cells:
            display_grid[row, col] = str(num)
            
        print(display_grid)