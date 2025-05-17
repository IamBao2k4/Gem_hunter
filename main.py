from gem_hunter import GemHunter
from typing import List, Tuple

def from_file(filename: str) -> Tuple[Tuple[int, int], List[Tuple[int, int, int]]]:

        numbered_cells = []
        rows = []
        
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                # Split the line and remove any whitespace
                cells = [cell.strip() for cell in line.split(',')]
                rows.append(len(cells))
                
                # Process each cell in the row
                for j, cell in enumerate(cells):
                    if cell != '_':  # If it's a number
                        numbered_cells.append((i, j, int(cell)))
        
        # Verify all rows have the same length
        if len(set(rows)) != 1:
            raise ValueError("All rows must have the same length")
            
        grid_size = (len(rows), rows[0])
        return grid_size, numbered_cells 

def main():
    grid_size, numbered_cells = from_file("./testcases/input_2.txt")

    game = GemHunter(grid_size, numbered_cells)
    
    print("Solving with PySAT...")
    success, solution, pysat_time = game.solve_with_pysat()
    if success:
        print("\nPySAT Solution:")
        game.display_solution(solution)
        print(f"Time taken: {pysat_time:.4f} seconds")
    
    print("\nSolving with Brute Force...")
    success, solution, brute_time = game.solve_brute_force()
    if success:
       print("\nBrute Force Solution:")
       game.display_solution(solution)
       print(f"Time taken: {brute_time:.4f} seconds")
    
    print("\nSolving with Backtracking...")
    success, solution, backtrack_time = game.solve_backtracking()
    if success:
        print("\nBacktracking Solution:")
        game.display_solution(solution)
        print(f"Time taken: {backtrack_time:.4f} seconds")
    
    print("\nPerformance Comparison:")
    print(f"PySAT: {pysat_time:.4f} seconds")
    print(f"Brute Force: {brute_time:.4f} seconds")
    print(f"Backtracking: {backtrack_time:.4f} seconds")

if __name__ == "__main__":
    main() 