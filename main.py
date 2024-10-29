# %%
from dd.autoref import BDD
import numpy as np
import time
import test_selection as ts
import pickle


# %% ===================================================================
# Defining the FSM in Table 1.
bdd = BDD()
#ts.initialize_bdd(bdd)

# Declare the mode variables
bdd.declare("on")
on = bdd.add_expr("on")
# Declare true and false
t = bdd.true
f = bdd.false

# Define the FSM
FSM = [[on, t, f, f], [f, t, t, t], [on, f, t, t]]

# Print the FSM
ts.print_table(FSM, bdd)

# %%
# Detectability analysis
det = ts.Detectability(FSM)
ts.print_det(det, bdd)

# %%
# Detectability analysis for a subset of residuals
det = ts.Detectability(ts.select_residuals(FSM, [0]))
ts.print_det(det, bdd)

# %%
# Isolability analysis
isol = ts.Isolability(FSM)
ts.print_table(isol, bdd)

# %%
# Isolability analysis for a subset of residuals
isol = ts.Isolability(ts.select_residuals(FSM, [0]))
ts.print_table(isol, bdd)

# %%
# Diagnosability analysis, i.e., detectability and isolability. This producecs the diagnosability matrix in (8).
diag = ts.Diagnosability(FSM)
ts.print_table(diag, bdd)

# %%
# Diagnosability analysis for a subset of residuals. This reproduces the diagnosability matrix in (7) for residual 1.
diag = ts.Diagnosability(ts.select_residuals(FSM, [0]))
ts.print_table(diag, bdd)

# %% Test selection achieving maximal diagnosability in all operation modes

Rs1, Imp1, diag_selected1 = ts.TestSelection(FSM, bdd)

print("Results with TestSelection:")
print("Selected residuals :", Rs1)
print("Residual importance:", Imp1)
print("Diagnosability of selected tests:")
ts.print_table(diag_selected1, bdd)

# %% Test selection, isolation in any mode

Rs2, Imp2, diag_selected2 = ts.TestSelectionAnyMode(FSM, bdd)

print("Results with TestSelectionAnyMode:")
print("Selected residuals :", Rs2)
print("Residual importance:", Imp2)
print("Diagnosability of selected tests:")
diag = ts.Diagnosability(ts.select_residuals(FSM, Rs2))
ts.print_table(diag, bdd)

# %% Test selection, counting assignments

nvars = len(bdd.vars)
Rs3, Imp3, diag_selected3 = ts.TestSelectionAssignments(FSM, nvars, bdd)

print("Results with TestSelectionAssignments:")
print("Selected residuals :", Rs3)
print("Residual importance:", Imp3)
print("Diagnosability of selected tests:")
ts.print_table(diag_selected3, bdd)

# %% =====================================================
# Define the fault signature matrix in Table 2 of a 2-module battery pack.

# Declare the mode variables
bdd = BDD()
bdd.declare("on1", "on2")
on1 = bdd.add_expr("on1")
on2 = bdd.add_expr("on2")

t = bdd.true
f = bdd.false

# Define the fault signature matrix
FSM = np.array(
    [
        [f, f, f, f, t, f, f, on2],
        [f, f, f, t, t, t, f, f],
        [f, f, f, t, f, t, f, on2],
        [f, t, f, f, f, f, f, on1],
        [t, t, t, f, f, f, f, f],
        [t, f, t, f, f, f, f, on1],
        [f, f, on1, f, f, on2, t, f],
        [f, f, on1, on2, on2, f, t, f],
        [f, f, on1, on2, f, f, t, on2],
        [on1, on1, f, f, f, on2, t, f],
        [on1, f, f, f, f, on2, t, on1],
        [on1, on1, f, on2, on2, f, t, f],
        [on1, on1, f, on2, f, f, t, on2],
        [on1, f, f, on2, on2, f, t, on1],
        [on1, f, f, on2, f, f, t, on1 | on2],
    ]
)

# In the paper the indexing of the residuals are based on underlying MSO sets according to the following list.
tests = [1, 2, 3, 4, 11, 12, 7, 8, 9, 15, 18, 16, 17, 20, 21]

print("FSM of 2-module battery pack:")
ts.print_table(FSM, bdd)

# %% Test selection  (6 test selected for 8 faults, 4 local and 2 global) in 44 ms
start_time = time.time()
Rs1, Imp1, diag_selected1 = ts.TestSelection(FSM, bdd)
end_time = time.time()
elapsed_time = end_time - start_time
selected_tests1 = [tests[r] for r in Rs1]

print("Results with TestSelection:")
print(f"Computation time: {elapsed_time:.6f} seconds")
print("Selected residuals :", selected_tests1)
print("Residual importance:", Imp1)
print("Diagnosability of selected tests:")
ts.print_table(diag_selected1, bdd)

# %% Test selection, isolation in any mode

start_time = time.time()
Rs2, Imp2, diag_selected2 = ts.TestSelectionAnyMode(FSM, bdd)
end_time = time.time()
elapsed_time2 = end_time - start_time
selected_tests2 = [tests[r] for r in Rs2]

print("Results with TestSelectionAnyMode:")
print(f"Computation time: {elapsed_time2:.6f} seconds")
print("Selected residuals :", selected_tests2)
print("Residual importance:", Imp2)
print("Diagnosability of selected tests:")
diag = ts.Diagnosability(ts.select_residuals(FSM, Rs2))
ts.print_table(diag, bdd)

# %% Test selection, counting assignments

nvars = len(bdd.vars)
start_time = time.time()
Rs3, Imp3, diag_selected3 = ts.TestSelectionAssignments(FSM, nvars, bdd)
end_time = time.time()
elapsed_time3 = end_time - start_time
selected_tests3 = [tests[r] for r in Rs3]

print("Results with TestSelectionAssignments:")
print(f"Computation time: {elapsed_time3:.6f} seconds")
print("Selected residuals :", selected_tests3)
print("Residual importance:", Imp3)
print("Diagnosability of selected tests:")
ts.print_table(diag_selected3, bdd)

# %% =================================================
# 2-module example where each module has two mode variables forward (fi) and backward (bi) such that:
#  f1 & ~b1 : forward connection mode of module 1
# ~f1 &  b1 : backward connection mode of module 1
# ~f1 & ~b1 : disconnected mode of module 1
#  f1 &  b1 : not valid mode of module 1

# Declare the mode variables:
bdd = BDD()
bdd.declare("f1", "b1", "f2", "b2")
f1 = bdd.add_expr("f1")
f2 = bdd.add_expr("f2")
b1 = bdd.add_expr("b1")
b2 = bdd.add_expr("b2")

# Declare invariant constraints:
constraint = ~(f1 & b1) & ~(f2 & b2)

# Define the fault signature matrix
on1 = (f1 | b1) & constraint
on2 = (f2 | b2) & constraint

t = constraint
f = bdd.false

FSM = np.array(
    [
        [f, f, f, f, t, f, f, on2],
        [f, f, f, t, t, t, f, f],
        [f, f, f, t, f, t, f, on2],
        [f, t, f, f, f, f, f, on1],
        [t, t, t, f, f, f, f, f],
        [t, f, t, f, f, f, f, on1],
        [f, f, on1, f, f, on2, t, f],
        [f, f, on1, on2, on2, f, t, f],
        [f, f, on1, on2, f, f, t, on2],
        [on1, on1, f, f, f, on2, t, f],
        [on1, f, f, f, f, on2, t, on1],
        [on1, on1, f, on2, on2, f, t, f],
        [on1, on1, f, on2, f, f, t, on2],
        [on1, f, f, on2, on2, f, t, on1],
        [on1, f, f, on2, f, f, t, on1 | on2],
    ]
)

# In the paper the indexing of the residuals are based on underlying MSO sets according to the following list.
tests = [1, 2, 3, 4, 11, 12, 7, 8, 9, 15, 18, 16, 17, 20, 21]

print("FSM of 2-module battery pack with forward and backward mode variables:")
ts.print_table(FSM, bdd)

# %% Test selection  (6 test selected for 8 faults, 4 local and 2 global)
# in 44 ms

start_time = time.time()
Rs1, Imp1, diag_selected1 = ts.TestSelection(FSM, bdd)
end_time = time.time()
elapsed_time = end_time - start_time
selected_tests1 = [tests[r] for r in Rs1]

print("Results with TestSelection:")
print(f"Computation time: {elapsed_time:.6f} seconds")
print("Selected residuals :", selected_tests1)
print("Residual importance:", Imp1)
print("Diagnosability of selected tests:")
#ts.print_table(ts.select_residuals(FSM, Rs1), bdd)
ts.print_table(diag_selected1,bdd)

# %% Test selection, isolation in any mode

start_time = time.time()
Rs2, Imp2, diag_selected2 = ts.TestSelectionAnyMode(FSM, bdd)
end_time = time.time()
elapsed_time2 = end_time - start_time
selected_tests2 = [tests[r] for r in Rs2]

print("Results with TestSelectionAnyMode:")
print(f"Computation time: {elapsed_time2:.6f} seconds")
print("Selected residuals :", selected_tests2)
print("Residual importance:", Imp2)
print("Diagnosability of selected tests:")
diag = ts.Diagnosability(ts.select_residuals(FSM, Rs2))
ts.print_table(diag, bdd)

# %% Test selection, counting assignments

nvars = len(bdd.vars)
start_time = time.time()
Rs3, Imp3, diag_selected3 = ts.TestSelectionAssignments(FSM, nvars, bdd)
end_time = time.time()
elapsed_time3 = end_time - start_time
selected_tests3 = [tests[r] for r in Rs3]

print("Results with TestSelectionAssignments:")
print(f"Computation time: {elapsed_time3:.6f} seconds")
print("Selected residuals :", selected_tests3)
print("Residual importance:", Imp3)
print("Diagnosability of selected tests:")
ts.print_table(diag_selected3, bdd)

# %% ======================================================
# 4 module example with 93 tests and 14 faults

# Initialize BDD
bdd = BDD()
bdd.declare("on1", "on2", "on3", "on4")
on1 = bdd.add_expr("on1")
on2 = bdd.add_expr("on2")
on3 = bdd.add_expr("on3")
on4 = bdd.add_expr("on4")

t = bdd.true
f = bdd.false
#    ts.initialize_bdd(bdd)

# Load 4-module FSM from file
with open("fsm_models.pkl", "rb") as file:
    models = pickle.load(file)

FSM_string = models["4_module"]
# Rebuild the BDD objects from the expression strings
FSM = [[bdd.add_expr(expr) for expr in row] for row in FSM_string]

print("Loaded FSM of 4-module battery pack.")
# ts.print_table(FSM, bdd)

# %% Test selection

start_time = time.time()
Rs1, Imp1, diag_selected1 = ts.TestSelection(FSM, bdd)
end_time = time.time()
elapsed_time = end_time - start_time

print("Results with TestSelection:")
print(f"Computation time: {elapsed_time:.6f} seconds")
print(f"{len(Rs1):d} residuals selected:", Rs1)
print("Residual importance:", Imp1)

# %% Test selection, isolation in any mode

start_time = time.time()
Rs2, Imp2, diag_selected2 = ts.TestSelectionAnyMode(FSM, bdd)
end_time = time.time()
elapsed_time2 = end_time - start_time

print("Results with TestSelectionAnyMode:")
print(f"Computation time: {elapsed_time2:.6f} seconds")
print(f"{len(Rs2):d} residuals selected:", Rs1)
print("Residual importance:", Imp2)

# %% Test selection, counting assignments

nvars = len(bdd.vars)
start_time = time.time()
Rs3, Imp3, diag_selected3 = ts.TestSelectionAssignments(FSM, nvars, bdd)
end_time = time.time()
elapsed_time3 = end_time - start_time

print("Results with TestSelectionAssignments:")
print(f"Computation time: {elapsed_time3:.6f} seconds")
print(f"{len(Rs3):d} residuals selected:", Rs1)
print("Residual importance:", Imp3)

# %% ======================================================
# 6 module example with 747 tests and 20 faults

# Initialize BDD
bdd = BDD()
bdd.declare("on1", "on2", "on3", "on4", "on5", "on6")
on1 = bdd.add_expr("on1")
on2 = bdd.add_expr("on2")
on3 = bdd.add_expr("on3")
on4 = bdd.add_expr("on4")
on5 = bdd.add_expr("on5")
on6 = bdd.add_expr("on6")

t = bdd.true
f = bdd.false
#    ts.initialize_bdd(bdd)

# Load 6-module FSM from file
with open("fsm_models.pkl", "rb") as file:
    models = pickle.load(file)

FSM_string = models["6_module"]
# Rebuild the BDD objects from the expression strings
FSM = [[bdd.add_expr(expr) for expr in row] for row in FSM_string]

print("Loaded FSM of 6-module battery pack.")
# ts.print_table(FSM, bdd)

# %% Test selection

start_time = time.time()
Rs1, Imp1, diag_selected1 = ts.TestSelection(FSM, bdd)
end_time = time.time()
elapsed_time = end_time - start_time

print("Results with TestSelection:")
print(f"Computation time: {elapsed_time:.6f} seconds")
print(f"{len(Rs1):d} residuals selected:", Rs1)
print("Residual importance:", Imp1)

# %% Test selection, isolation in any mode

start_time = time.time()
Rs2, Imp2, diag_selected2 = ts.TestSelectionAnyMode(FSM, bdd)
end_time = time.time()
elapsed_time2 = end_time - start_time

print("Results with TestSelectionAnyMode:")
print(f"Computation time: {elapsed_time2:.6f} seconds")
print(f"{len(Rs2):d} residuals selected:", Rs2)
print("Residual importance:", Imp2)

# %% Test selection, counting assignments

nvars = len(bdd.vars)
start_time = time.time()
Rs3, Imp3, diag_selected3 = ts.TestSelectionAssignments(FSM, nvars, bdd)
end_time = time.time()
elapsed_time3 = end_time - start_time

print("Results with TestSelectionAssignments:")
print(f"Computation time: {elapsed_time3:.6f} seconds")
print(f"{len(Rs3):d} residuals selected:", Rs3)
print("Residual importance:", Imp3)


# %%
