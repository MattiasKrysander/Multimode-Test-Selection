from functools import reduce
from tabulate import tabulate

# Detectability analysis
def Detectability(FSM):
    """
    Computes the detectability of faults based on the Fault Signature Matrix (FSM).

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.

    Returns:
        list of bdds: A list where each element corresponds to a fault. Each element is a Boolean function from the system operation modes to T/F indicating the detectability of the fault accross the operation modes. 
    """
    # Initialize
    no_tests = len(FSM)
    no_faults = len(FSM[0])
    det = [0] * no_faults

    # Compute the bitwise OR across each column in FSM
    for j in range(no_faults):
        det[j] = reduce(lambda x, y: x | y, (FSM[i][j] for i in range(no_tests)))
    return det


# Isoability analysis
def Isolability(FSM):
    """
    Computes the isolability matrix for a given Fault Signature Matrix (FSM).

    The isolability matrix indicates which faults can be isolated from each other
    based on the given FSM. 

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.

    Returns:
        list of list of bdds: A 2D list representing the isolability matrix. Each element (i, j) is a Boolean function across the operation modes that indicates whether fault i can be isolated from fault j in the different modes. If the Boolean function evaluates to True for an operation mode m, then fault i can be isolated from fault j in m. If the Boolean function evaluates to False for m, then fault i cannot be isolated from fault j in m.
    """
    # Initialize
    no_tests = len(FSM)
    no_faults = len(FSM[0])
    isol = [[0] * no_faults for _ in range(no_faults)]

    # Compute the bitwise OR across each column in FSM
    for j in range(no_faults):
        for k in range(no_faults):
            isol[j][k] = reduce(lambda x, y: x | y, (FSM[i][j] & ~FSM[i][k] for i in range(no_tests)))

    return isol


def Diagnosability(FSM):
    """
    Computes the diagnosability matrix for a given Fault Signature Matrix (FSM).

    The diagnosability matrix is constructed using detectability and isolability
    information for each fault in the FSM.

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.

 
    Returns:
        list of list of bdds: A 2D list representing the diagnosability matrix. The diagnosability matrix is a combination of the detectability and isolability matrix. If the number of faults is n, the diagnosability matrix is an n x (n+1) matrix. The first column corresponds to the detectability of each fault. The remaining columns correspond to the isolability of each fault from the other faults. 
    """
    # Initialize
    no_faults = len(FSM[0])
    det = Detectability(FSM)
    isol = Isolability(FSM)

    diagnosability = []
    # Construct the diagnosability matrix
    for i in range(no_faults):
        # Construct each row
        row = [det[i]] + isol[i]
        diagnosability.append(row)

    return diagnosability


# Select residuals
def select_residuals(FSM, rows):
    return [FSM[i] for i in rows]


def print_table(FSM, bdd):
    """
    Prints a Fault Signature Matrix (FSM) as a table using the tabulate library.

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.
        bdd (BDD): A binary decision diagram (BDD) object used to convert FSM elements to expressions.

    Returns:
        None
    """
    # Convert the data to the format required by tabulate
    formatted_data = [[str(bdd.to_expr(col)) for col in row] for row in FSM]
    # Print the table
    print(tabulate(formatted_data, tablefmt="grid"))


def print_det(det, bdd):
    """
    Prints a table of Boolean expressions represented in a Binary Decision Diagram (BDD) format.

    Args:
        det (list): A list of rows where each row represents a Boolean expression in Binary Decision Diagram (BDD)      format representing the detectability of a fault.
        bdd (BDD object): An object that has a `to_expr` method, which converts a BDD row into a human-readable Boolean expression.

    Returns:
        None
    """
    # Convert the data to the format required by tabulate
    formatted_data = [[str(bdd.to_expr(row))] for row in det]
    # Print the table
    print(tabulate(formatted_data, tablefmt="grid"))


def TestSelection(FSM, bdd):
    """
    Selects a set of residuals given a Fault Signature Matrix (FSM) with maximum diagnosability.

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.
        bdd (BDD): A binary decision diagram (BDD) object used to convert FSM elements to expressions.

    Returns:
    tuple:
        - Rs (list): A list of indices representing the selected residuals that maximize diagnosability.
        - Imp (list): A list of improvement values corresponding to each selected residual, showing the diagnosability gain achieved by selecting that residual.
        - diag_selected (list): The final diagnosability matrix representing combined diagnosability of all selected residuals.

    Description:
    The `TestSelection` function iteratively selects residuals that provide the highest diagnosability 
    improvement based on the diagnosability matrix. The function continues until no residual provides further 
    diagnosability improvement.

    Steps:
    1. Initialize `Rs` (selected residuals), `Imp` (improvement values), and `Rr` (remaining residuals).
    2. Compute diagnosability matrices for each residual in the FSM using a `Diagnosability` function.
    3. For each remaining residual, calculate the diagnosability improvement if selected.
    4. Choose a residual with the highest improvement and update the selected diagnosability matrix.
    5. Repeat the selection process until no further improvement is possible.

    Example:
    >>> FSM = [...]  # Define the FSM with residuals
    >>> selected_residuals, improvements, diag_matrix = TestSelection(FSM)
    >>> print("Selected Residuals:", selected_residuals)
    >>> print("Improvements:", improvements)
    >>> print("Diagnosability Matrix:", diag_matrix)

    Notes:
    - `Diagnosability` is assumed to be a function that computes diagnosability for each residual.
    - `f` is assumed to represent a `False` or `fault-free` state in the diagnosability matrix, where improvement is determined.
    """
    # Initialize
    no_tests = len(FSM)

    # Initialize the set of residuals to be selected
    Rs = []  # Selected residuals
    Imp = []  # Improvement
    Rr = list(range(no_tests))  # Remaining residuals

    # Compute the diagnosability matrix for all residuals
    # diag = Diagnosability(FSM)
    # Initialize the diagnosability of the selected residuals
    rows = len(FSM[0])
    cols = rows + 1
    diag_selected = [[bdd.false] * cols for _ in range(rows)]
    # Compute the diagnosability matrix for all residuals
    res_diag = [Diagnosability([res]) for res in FSM]

    while Rr != []:  # While there are residuals to be selected
        improvement = [0] * len(Rr)  # Initialize the improvement for each residual
        for i in range(len(Rr)):  # For each remaining residual
            result = [[a & ~b for a, b in zip(row1, row2)] for row1, row2 in zip(res_diag[Rr[i]], diag_selected)]
            # Count entries that are not False using list comprehension
            improvement[i] = sum(1 for row in result for value in row if value != bdd.false)
        max_imp = max(improvement)
        if max_imp == 0:
            break
        index_of_max = improvement.index(max_imp)
        # select the first residual with the highest improvement
        diag_selected = [
            [a | b for a, b in zip(row1, row2)] for row1, row2 in zip(res_diag[Rr[index_of_max]], diag_selected)
        ]
        Rs.append(Rr[index_of_max])
        Rr.remove(Rs[-1])
        Imp.append(max_imp)
    return Rs, Imp, diag_selected



def TestSelectionAnyMode(FSM, bdd):
    """
    Selects a set of residuals given a Fault Signature Matrix (FSM) with maximum diagnosability when considering a diagnosability property fulfilled if it is satisfied in any mode.

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.
        bdd (BDD): A binary decision diagram (BDD) object used to convert FSM elements to expressions.

    Returns:
    tuple:
        - Rs (list): A list of indices representing the selected residuals that maximize diagnosability.
        - Imp (list): A list of improvement values corresponding to each selected residual, showing the diagnosability gain achieved by selecting that residual.
        - diag_selected (list): A binary diagnosability matrix representing the combined diagnosability of all selected residuals. If an entry is True, there exist a mode where the corresponding diagnosability property is satisfied. 
    """

    # Initialize
    no_tests = len(FSM)
    # Initialize the set of residuals to be selected
    Rs = []
    Imp = []
    Rr = list(range(no_tests))

    # Compute the diagnosability matrix for all residuals
    # diag = Diagnosability(FSM)
    # Initialize the diagnosability of the selected residuals
    rows = len(FSM[0])
    cols = rows + 1
    diag_selected = [[bdd.false] * cols for _ in range(rows)]
    # Compute the diagnosability matrix for all residuals
    res_diag = [Diagnosability([res]) for res in FSM]
    # One additional row to require diagnosability of any mode
    res_diag = [[[bdd.true if element != bdd.false else bdd.false for element in row] for row in res] for res in res_diag]

    while Rr != []:
        improvement = [0] * len(Rr)
        for i in range(len(Rr)):
            result = [[a & ~b for a, b in zip(row1, row2)] for row1, row2 in zip(res_diag[Rr[i]], diag_selected)]
            # Count entries that are not False using list comprehension
            improvement[i] = sum(1 for row in result for value in row if value != bdd.false)
        max_imp = max(improvement)
        if max_imp == 0:
            break
        index_of_max = improvement.index(max_imp)
        # select the first residual with the highest improvement
        diag_selected = [
            [a | b for a, b in zip(row1, row2)] for row1, row2 in zip(res_diag[Rr[index_of_max]], diag_selected)
        ]
        Rs.append(Rr[index_of_max])
        Rr.remove(Rs[-1])
        Imp.append(max_imp)
    return Rs, Imp, diag_selected


def TestSelectionAssignments(FSM, nvars, bdd):
    """
    Selects a set of residuals given a Fault Signature Matrix (FSM) with maximum diagnosability in all modes. This function evaluates diagnosability improvement based on the number of additional mode assignments that satisfy the diagnosability properties. 

    Args:
        FSM (list of list of bdds): A 2D list representing the Fault Signature Matrix where each row corresponds to a test and each column corresponds to a fault. Each element is a Boolean function indicating the presence (1) or absence (0) of fault detection by the test accross the operation modes.
        bdd (BDD): A binary decision diagram (BDD) object used to convert FSM elements to expressions.

    Returns:
    tuple:
        - Rs (list): A list of indices representing the selected residuals that maximize diagnosability.
        - Imp (list): A list of improvement values corresponding to each selected residual, showing the diagnosability gain achieved by selecting that residual.
        - diag_selected (list): The final diagnosability matrix representing combined diagnosability of all selected residuals.
    """
    # Initialize
    no_tests = len(FSM)
    # Initialize the set of residuals to be selected
    Rs = []
    Imp = []
    Rr = list(range(no_tests))

    # Compute the diagnosability matrix for all residuals
    # diag = Diagnosability(FSM)
    # Initialize the diagnosability of the selected residuals
    rows = len(FSM[0])
    cols = rows + 1
    diag_selected = [[bdd.false] * cols for _ in range(rows)]
    # Compute the diagnosability matrix for all residuals
    res_diag = [Diagnosability([res]) for res in FSM]

    while Rr != []:
        improvement = [0] * len(Rr)
        for i in range(len(Rr)):
            result = [[a & ~b for a, b in zip(row1, row2)] for row1, row2 in zip(res_diag[Rr[i]], diag_selected)]
            # Only this line changed
            improvement[i] = sum(bdd.count(value, nvars) for row in result for value in row)
        max_imp = max(improvement)
        if max_imp == 0:
            break
        index_of_max = improvement.index(max_imp)
        # select the first residual with the highest improvement
        diag_selected = [
            [a | b for a, b in zip(row1, row2)] for row1, row2 in zip(res_diag[Rr[index_of_max]], diag_selected)
        ]
        Rs.append(Rr[index_of_max])
        Rr.remove(Rs[-1])
        Imp.append(max_imp)
    return Rs, Imp, diag_selected
