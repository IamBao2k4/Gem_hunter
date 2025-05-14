from gem_hunter import GemHunter

def main():
    grid_size, numbered_cells = GemHunter.from_file("./testcases/input_3.txt")

    game = GemHunter(grid_size, numbered_cells)
    
    print("Solving with PySAT...")
    success, solution, pysat_time = game.solve_with_pysat()
    if success:
        print("\nPySAT Solution:")
        game.display_solution(solution)
        print(f"Time taken: {pysat_time:.4f} seconds")
    
    # print("\nSolving with Brute Force...")
    # success, solution, brute_time = game.solve_brute_force()
    # if success:
    #    print("\nBrute Force Solution:")
    #    game.display_solution(solution)
    #    print(f"Time taken: {brute_time:.4f} seconds")
    
    print("\nSolving with Backtracking...")
    success, solution, backtrack_time = game.solve_backtracking()
    if success:
        print("\nBacktracking Solution:")
        game.display_solution(solution)
        print(f"Time taken: {backtrack_time:.4f} seconds")
    
    print("\nPerformance Comparison:")
    print(f"PySAT: {pysat_time:.4f} seconds")
    #print(f"Brute Force: {brute_time:.4f} seconds")
    print(f"Backtracking: {backtrack_time:.4f} seconds")

if __name__ == "__main__":
    main() 