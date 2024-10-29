
## Test Selection for Diagnosing Multimode Systems

### Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Files](#files)
4. [Quick Start](#quick-start)
5. [Usage](#usage)
6. [License](#license)

---

### Overview
This Python project provides functions for analyzing and selecting tests given a multimode fault signature matrix (FSM), specifically for systems with multiple operating modes. It allows users to efficiently choose a small set of  test, with maximum fault detectability and isolability across all system operation modes. For a detailed description see [paper](). 

The software is freely available under an MIT license. If you use this software in your research, please cite:

Mattias Krysander and Fatemeh Hashemniya. "Test Selection for Diagnosing Multimode Systems" (https://doi.org/), The 35th International Conference on Principles of Diagnosis and Resilient Systems (DX'24),  Vienna, Austria, 2024.

### Features
- **Multimode Analysis**: Supports FSMs with multiple operating modes.
- **Optimized Test Selection**: Greedy algorithms to select small set of tests with maximum fault diagnosability across all operation modes.
- **Visualization**: Functions to print multimode FSM and Diagnosability matrices.
- **Compatibility with BDD**: Allows the use of Binary Decision Diagrams (BDD) for efficient computation and representation.

### Files 

Here’s an overview of the main files in this repository:

- `test_selection.py`: Contains all functions needed for test selection in FSMs.
- `main.py`: A script demonstrating how to use the test selection functions with sample FSMs. All examples from the paper is run.
- `fsm_models.pkl`: Contains the FSMs of the 4 and 6 module battery packs analyzed in the paper.

### Quick Start
To try out the test selection functions, run the `main.py` script:

```bash
python main.py
```

### Usage

Below is an example from main.py of defining a multimode FSM and using a test selection function in test_selection.py:

```python
from dd.autoref import BDD
import test_selection as ts

# Defining the FSM in Table 1.
bdd = BDD()
ts.initialize_bdd(bdd)

# Declare the mode variables
bdd.declare('on')
on = bdd.add_expr('on')

# Declare true and false
t = bdd.true
f = bdd.false

# Define the FSM
FSM = [[on, t, f, f],
       [f,  t, t, t],
       [on, f, t, t]]

# Test selection achieving maximal diagnosability in all operation modes

Rs1, Imp1, diag_selected1 = ts.TestSelection(FSM)

print("Results with TestSelection:")
print("Selected residuals :",Rs1)
print("Residual importance:",Imp1)
print("Diagnosability of selected tests:")
ts.print_table(diag_selected1,bdd)

```

### License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.





