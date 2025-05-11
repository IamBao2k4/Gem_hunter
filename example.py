from gem_hunter import GemHunter

def main():
    # Create a 5x5 grid with some numbered cells
    grid_size = (5, 5)

    numbered_cells = [
        (0, 0, 2),  # First row: 2 T T 1 G
        (0, 3, 1),
        (1, 1, 5),  # Second row: T 5 4 2 G
        (1, 2, 4),
        (1, 3, 2),
        (2, 0, 3),  # Third row: 3 T T 2 1
        (2, 3, 2),
        (2, 4, 1),
        (3, 0, 3),  # Fourth row: 3 T 6 T 1
        (3, 2, 6),
        (3, 4, 1),
        (4, 0, 2),  # Fifth row: 2 T T 2 1
        (4, 3, 2),
        (4, 4, 1)
    ]

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