import numpy as np
from typing import List, Tuple, Set
import time
from pysat.solvers import Glucose3
from pysat.formula import CNF
from itertools import combinations

class GemHunter:
    def __init__(self, grid_size: Tuple[int, int], numbered_cells: List[Tuple[int, int, int]]):
        """
        Initialize the Gem Hunter game.
        
        Args:
            grid_size: Tuple of (rows, cols) for the grid
            numbered_cells: List of (row, col, number) tuples representing numbered cells
        """
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
        
    def _create_variable_mapping(self):
        """Create mapping between grid positions and CNF variables."""
        var_id = 1
        for i in range(self.rows):
            for j in range(self.cols):
                self.var_mapping[(i, j)] = var_id
                self.reverse_mapping[var_id] = (i, j)
                var_id += 1
                
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get valid neighboring cells for a given position."""
        neighbors = []
        for i in range(max(0, row-1), min(self.rows, row+2)):
            for j in range(max(0, col-1), min(self.cols, col+2)):
                if (i, j) != (row, col):
                    neighbors.append((i, j))
        return neighbors
    
    def generate_cnf(self) -> CNF:
        """Generate CNF clauses for the game."""
        cnf = CNF()
        
        # For each numbered cell, create constraints
        for row, col, num in self.numbered_cells:
            neighbors = self.get_neighbors(row, col)
            neighbor_vars = [self.var_mapping[n] for n in neighbors]
            
            # Create clauses for exactly 'num' traps
            # For each subset of size num+1, at least one must be a gem
            if num + 1 <= len(neighbor_vars):
                for trap_positions in combinations(neighbor_vars, num + 1):
                    cnf.append([-v for v in trap_positions])
            
            # For each subset of size len(neighbors)-num+1, at least one must be a trap
            if len(neighbor_vars) - num + 1 > 0:
                for trap_positions in combinations(neighbor_vars, len(neighbor_vars) - num + 1):
                    cnf.append(trap_positions)
        
        return cnf
    
    def solve_with_pysat(self) -> Tuple[bool, List[int], float]:
        """Solve the game using pysat."""
        cnf = self.generate_cnf()
        solver = Glucose3()
        solver.append_formula(cnf)
        
        start_time = time.time()
        solution = solver.solve()
        end_time = time.time()
        
        if solution:
            model = solver.get_model()
            # Convert model to the same format as other solvers
            assignment = [0] * (self.rows * self.cols)
            for var in model:
                if abs(var) <= len(assignment):
                    assignment[abs(var)-1] = 1 if var > 0 else -1
            return True, assignment, end_time - start_time
        return False, None, end_time - start_time
    
    def solve_brute_force(self) -> Tuple[bool, List[int], float]:
        """Solve the game using brute force approach."""
        start_time = time.time()
        n_vars = self.rows * self.cols
        
        # Try all possible combinations
        for i in range(2 ** n_vars):
            assignment = []
            temp = i
            for _ in range(n_vars):
                assignment.append(1 if temp % 2 else -1)
                temp //= 2
            
            if self._is_valid_assignment(assignment):
                end_time = time.time()
                return True, assignment, end_time - start_time
                
        end_time = time.time()
        return False, None, end_time - start_time
    
    def _is_valid_assignment(self, assignment: List[int]) -> bool:
        """Check if an assignment satisfies all constraints."""
        for row, col, num in self.numbered_cells:
            neighbors = self.get_neighbors(row, col)
            trap_count = sum(1 for n in neighbors if assignment[self.var_mapping[n]-1] > 0)
            if trap_count != num:
                return False
        return True
    
    def solve_backtracking(self) -> Tuple[bool, List[int], float]:
        """Solve the game using backtracking approach."""
        start_time = time.time()
        n_vars = self.rows * self.cols
        assignment = [0] * n_vars
        
        def backtrack(pos: int) -> bool:
            if pos == n_vars:
                return self._is_valid_assignment(assignment)
            
            # Try setting current position to trap
            assignment[pos] = 1
            if backtrack(pos + 1):
                return True
                
            # Try setting current position to gem
            assignment[pos] = -1
            if backtrack(pos + 1):
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
        """Display the solution grid."""
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