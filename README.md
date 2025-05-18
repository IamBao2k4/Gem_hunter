# 📦 Gem Hunter

A Python project that solves the **Gem Hunter** puzzle using three different algorithms: **PySAT (SAT solver)**, **brute force**, and **backtracking**.

---

## 📘 Overview

**Gem Hunter** is a logic puzzle played on a grid. Each cell may:

- Be **empty** (`_`)
- Contain a **number** (indicating how many traps are adjacent)
- Be determined as a **trap (`T`)** or **gem (`G`)**

🎯 The goal is to fill the grid so that:

- All numbered cells are satisfied
- All unknown (`_`) cells are assigned as either traps or gems

---

## ✨ Features

- 🔄 **Three solving algorithms**:
  - SAT Solver using **PySAT (Glucose3)**
  - **Brute-force** search
  - **Backtracking** search

- 📐 Supports grids of **various sizes** (small, medium, large)
- 🧪 Includes **test cases** and **output comparison**

---

## 🛠 Requirements

- Python 3.7+
- `python-sat`
- `numpy`

📦 Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
gem_hunter.py      # Main game logic and solvers
main.py            # Runs all solvers on all testcases
requirements.txt   # Python dependencies
testcases/         # Input and output files for test cases
README.md          # Project documentation
```

---

## 📄 File Formats

### 🧾 Input Files
- Located in `testcases/` and named `input_x.txt`
- Each line is a row, cells separated by commas
- Use `_` for unknown cells, numbers for clue cells

**Example:**
```
3,_,2,_
_,_,2,_
_,3,1,_
```

### 🧾 Output Files
- Located in `testcases/` and named `output<Method>_x.txt`
- Same format as input, but unknowns replaced with:
  - `'T'` (trap)
  - `'G'` (gem)
- Numbers are preserved

**Example:**
```
3,T,2,G
T,T,2,G
T,3,1,G
```

---

## ▶️ How to Use

### Run all solvers on all test cases:
```bash
python main.py
```

### Output:
- For each input file, the program prints the result for each algorithm
- Writes the result to a corresponding file, e.g., `outputPySAT_1.txt`

---

## 🧠 Algorithms

### 1. 🧩 PySAT Solver
- Converts the puzzle into a **CNF formula**
- Uses **Glucose3 SAT solver**
- ✅ Best for **large and complex** grids

### 2. 🚀 Brute Force
- Tries all possible assignments for unknown cells
- ✅ Guarantees a solution if one exists
- ❌ Only practical for **small grids**

### 3. 🔁 Backtracking
- Recursively assigns values
- Prunes invalid assignments early
- ✅ More efficient than brute force for **medium-sized** grids

---

## 🧪 Test Cases

| File Name              | Size      |
|------------------------|-----------|
| `input_1.txt`          | 5x5 grid  |
| `input_2.txt`          | 10x10 grid |
| `input_3.txt`          | 20x20 grid |

Each input file has a corresponding output for each algorithm.

---

## 📄 License

This project is open source and available under the **MIT License**.