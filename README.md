# Gem Hunter Game

A Python implementation of the Gem Hunter game using Conjunctive Normal Form (CNF) and various solving algorithms.

## Description

In this game, players explore a grid to find hidden gems while avoiding traps. Each numbered cell in the grid represents the number of traps surrounding it (horizontally, vertically, or diagonally). The game is solved using three different approaches:

1. CNF with PySAT Library
2. Brute Force Algorithm
3. Backtracking Algorithm

## Requirements

- Python 3.7+
- Required packages (install using `pip install -r requirements.txt`):
  - python-sat
  - numpy

## Project Structure

```
gem_hunter/
├── gem_hunter.py      # Main game implementation
├── generate_testcases.py  # Script to generate test cases
├── run_tests.py       # Script to run and compare algorithms
├── example.py         # Example usage
├── requirements.txt   # Package dependencies
├── testcases/        # Test cases directory
│   ├── input 1.txt   # 5x5 grid test case
│   ├── output 1.txt
│   ├── input 2.txt   # 11x11 grid test case
│   ├── output 2.txt
│   ├── input 3.txt   # 20x20 grid test case
│   └── output 3.txt
└── README.md         # This file
```

## File Format

### Input Files
- Named as "input x.txt" where x is the test case number
- Each cell is separated by commas
- '_' represents empty cells
- Numbers represent the count of surrounding traps

Example input:
```
3,_,2,_
_,_,2,_
_,3,1,_
```

### Output Files
- Named as "output x.txt" where x is the test case number
- 'T' represents traps
- 'G' represents gems
- Numbers from input are preserved

Example output:
```
3,T,2,G
T,T,2,G
T,3,1,G
```

## Implementation Details

### CNF Formulation
The game is formulated as a CNF problem where:
1. Each cell is represented by a boolean variable:
   - True (T): The cell contains a trap
   - False (G): The cell contains a gem
2. For each numbered cell with value n:
   - At least n neighboring cells must be traps
   - At most n neighboring cells can be traps

### Solving Methods

1. **PySAT Solver**:
   - Uses the Glucose3 SAT solver
   - Converts game constraints to CNF clauses
   - Generally fastest for complex puzzles

2. **Brute Force**:
   - Tries all possible combinations
   - Guarantees finding a solution if one exists
   - Becomes impractical for large grids

3. **Backtracking**:
   - Systematically explores possible assignments
   - More efficient than brute force
   - Can handle medium-sized grids effectively

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run example:
```bash
python example.py
```

3. Generate test cases:
```bash
python generate_testcases.py
```

4. Run performance comparison:
```bash
python run_tests.py
```

## Performance Analysis

The implementation includes three test cases of different sizes:
1. 5x5 grid (small)
2. 11x11 grid (medium)
3. 20x20 grid (large)

Typical performance comparison:
- PySAT: Most efficient for all grid sizes
- Backtracking: Good for small/medium grids
- Brute Force: Only practical for small grids

## License

This project is open source and available under the MIT License. 