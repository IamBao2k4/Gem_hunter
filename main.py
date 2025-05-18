import glob
from gem_hunter import GemHunter

if __name__ == '__main__':
    # Find all input files in 'testcase/' directory
    input_files = sorted(glob.glob('testcases/input_2.txt'))
    methods = [
        ('PySAT',    GemHunter.solve_with_sat),
        ('Backtracking', GemHunter.solve_with_backtracking),
        ('Brute-Force', GemHunter.solve_with_bruteforce)     
    ]

    for inp in input_files:
        print(f"=== Solving {inp} ===")
        game = GemHunter(inp)
        for name, method in methods:
            grid_out, elapsed, success = method(game)
            print(f"[{name}] Success: {success}, Time: {elapsed:.4f}s")
            game.print_grid(grid_out)
            if success:
                game.write_output(grid_out)
            print()  # blank line between methods
