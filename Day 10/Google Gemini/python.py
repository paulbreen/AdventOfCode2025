import re
import time
from typing import List, Tuple, Dict, Set, Deque
from collections import deque

# --- Parsing Logic ---

def parse_input(filename: str) -> List[Dict]:
    """
    Reads and parses the input file into a list of machine configurations.
    
    Each line is parsed into:
    - 'target_lights': The target state of indicator lights (0 for '.', 1 for '#').
    - 'buttons': A list of sets, where each set contains the indices of lights/counters
                 toggled/affected by that button.
    - 'joltage_targets': The required joltage levels (used for Part 2).
    """
    machines = []
    # Regex to capture the three main components of a line
    # [Lights] (B1)(B2)... {Joltages}
    line_pattern = re.compile(r'\[(.*?)\]\s*(.*?)\s*\{(.*?)\}')
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = line_pattern.match(line)
                if not match:
                    continue
                
                lights_str, buttons_str, joltage_str = match.groups()
                
                # 1. Parse Lights/Target Vector (0 or 1)
                target_lights = [1 if c == '#' else 0 for c in lights_str]
                
                # 2. Parse Buttons/Matrix A (Set of affected indices)
                # Matches (0,1,3)
                button_indices = re.findall(r'\((.*?)\)', buttons_str)
                buttons = []
                for idx_list_str in button_indices:
                    # An empty string in the parentheses means no indices affected
                    if idx_list_str:
                        indices = set(map(int, idx_list_str.split(',')))
                    else:
                        indices = set()
                    buttons.append(indices)
                
                # 3. Parse Joltage Targets (Integer vector)
                joltage_targets = list(map(int, joltage_str.split(',')))
                
                # Sanity check for problem structure consistency
                if len(target_lights) != len(joltage_targets):
                    print(f"Warning: Light count ({len(target_lights)}) != Joltage count ({len(joltage_targets)}) on line: {line}")
                
                machines.append({
                    'target_lights': target_lights,
                    'buttons': buttons,
                    'joltage_targets': joltage_targets,
                })
                
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        exit(1)
        
    return machines

# --- Part 1: Gaussian Elimination over Z_2 and Minimal Press Search ---

def solve_system_z2(num_lights: int, num_buttons: int, buttons: List[Set[int]], target: List[int]) -> int:
    """
    Solves A*x = b over Z_2 (x in {0, 1}) to find the solution with the minimum number of presses (min sum(x_i)).
    """
    # Create the Augmented Matrix [A | b]
    # Dimensions: L rows (lights), B+1 columns (buttons + target)
    aug_matrix = [
        [0] * (num_buttons + 1) for _ in range(num_lights)
    ]
    
    # Populate A and b
    for r in range(num_lights):
        for c in range(num_buttons):
            # A[r][c] is 1 if button 'c' affects light 'r'
            if r in buttons[c]:
                aug_matrix[r][c] = 1
        # b is the target light state
        aug_matrix[r][num_buttons] = target[r]

    # Gaussian Elimination over Z_2
    lead = 0
    for r in range(num_lights):
        if lead >= num_buttons:
            break
            
        i = r
        # Find the row with a 1 in the current leading column
        while i < num_lights and aug_matrix[i][lead] == 0:
            i += 1
            
        if i < num_lights:
            # Swap rows r and i
            aug_matrix[r], aug_matrix[i] = aug_matrix[i], aug_matrix[r]
            
            # Eliminate other 1s in the current column (lead)
            for i_elim in range(num_lights):
                if i_elim != r and aug_matrix[i_elim][lead] == 1:
                    # XOR row r into row i_elim
                    for j in range(lead, num_buttons + 1):
                        aug_matrix[i_elim][j] ^= aug_matrix[r][j]
            
            lead += 1
        
    # Check for inconsistency (0 = 1)
    for r in range(num_lights):
        # A row is inconsistent if all A coefficients are 0 but b is 1
        is_all_zero_row = all(aug_matrix[r][c] == 0 for c in range(num_buttons))
        if is_all_zero_row and aug_matrix[r][num_buttons] == 1:
            return float('inf') 

    # Determine Pivot and Free Columns
    pivot_cols = []
    row_for_col = {} # Maps pivot column index to the row index of its leading 1
    r = 0
    for c in range(num_buttons):
        if r < num_lights and aug_matrix[r][c] == 1:
            pivot_cols.append(c)
            row_for_col[c] = r
            r += 1

    free_cols = [c for c in range(num_buttons) if c not in pivot_cols]
    
    # 1. Particular Solution (xp)
    xp = [0] * num_buttons
    for c_pivot in pivot_cols:
        r_pivot = row_for_col[c_pivot]
        # xp[c_pivot] is the value in the augmented column for this pivot row
        xp[c_pivot] = aug_matrix[r_pivot][num_buttons]

    # 2. Null Space Basis (null_basis)
    null_basis = []
    for c_free in free_cols:
        v = [0] * num_buttons
        v[c_free] = 1 # Set the free variable to 1
        
        # Back-substitute to find the values of pivot variables
        for c_pivot in pivot_cols:
            r_pivot = row_for_col[c_pivot]
            # Since the matrix is in reduced row echelon form (RREF), 
            # the pivot variable's value is simply the coefficient in front of the 
            # free variable in the pivot row, XORed with other free variables.
            # In Z2, since we only set one free var to 1, we just take the coefficient.
            # The coefficient is aug_matrix[r_pivot][c_free]. The sign is implicitly handled by Z2 arithmetic.
            v[c_pivot] = aug_matrix[r_pivot][c_free] 
            
        null_basis.append(v)

    # 3. Find the minimum weight solution: x = xp + sum(a_i * v_i) over Z_2
    min_presses = float('inf')
    num_free = len(free_cols)
    
    # Iterate through all 2^num_free combinations of null space vectors
    for i in range(1 << num_free):
        current_x = list(xp)
        
        # Add null space vectors based on combination 'i'
        for j in range(num_free):
            if (i >> j) & 1: # If the j-th bit is set
                # Add (XOR) the j-th null vector to the current solution
                for k in range(num_buttons):
                    current_x[k] ^= null_basis[j][k]
        
        # Calculate total presses (weight) for the current solution
        current_presses = sum(current_x)
        min_presses = min(min_presses, current_presses)
        
    return min_presses

def puzzle_1_solve(machines: List[Dict]) -> int:
    """Calculates the fewest total presses for all machines for Part 1."""
    total_presses = 0
    
    for machine in machines:
        target = machine['target_lights']
        buttons = machine['buttons']
        num_lights = len(target)
        num_buttons = len(buttons)
        
        if num_lights == 0 or num_buttons == 0:
            return float('inf') 
            
        presses = solve_system_z2(num_lights, num_buttons, buttons, target)
        
        if presses == float('inf'):
            return float('inf') 
            
        total_presses += presses
        
    return total_presses

# --- Part 2: BFS for Minimal Sum Integer Solution (FIXED) ---

def solve_system_z_minimal_sum(num_lights: int, num_buttons: int, buttons: List[Set[int]], target: List[int]) -> int:
    """
    Solves A*x = b over Z (x >= 0) to find the minimum sum(x_i) using BFS.
    This is feasible because button effects only increase joltage (no toggling/decrease).
    """
    
    # 1. Correctly construct button effect vectors (the columns of A).
    # button_effects[j] is the vector (length num_lights) of changes to all joltage counters
    # when button j is pressed.
    button_effects: List[Tuple[int, ...]] = []
    for c in range(num_buttons): # Loop over buttons (index c)
        effect_vector = []
        for r in range(num_lights): # Loop over lights/counters (index r)
            # joltage counter 'r' is affected by button 'c'
            # Each press increases the counter by 1 if affected, 0 otherwise.
            effect_vector.append(1 if r in buttons[c] else 0) 
        
        button_effects.append(tuple(effect_vector))
        
    target_tuple = tuple(target)
    initial_state = tuple([0] * num_lights)

    if initial_state == target_tuple:
        return 0

    # Dijkstra's/BFS-like search
    # Cost to reach a state (current_joltage_tuple)
    min_presses: Dict[Tuple[int, ...], int] = {initial_state: 0}
    
    # Queue: (current_joltage_tuple) - using deque for efficient popleft
    queue: Deque[Tuple[int, ...]] = deque([initial_state]) 
    
    while queue:
        current_state = queue.popleft()
        current_cost = min_presses[current_state]

        # Try pushing each button
        for button_idx in range(num_buttons):
            # button_effect has length num_lights
            button_effect = button_effects[button_idx]
            
            # Calculate next state
            next_state_list = list(current_state)
            is_valid_transition = True
            
            for i in range(num_lights):
                # FIX: button_effect is now correctly indexed by i (0 to num_lights-1)
                next_state_list[i] += button_effect[i] 
                
                # Pruning: If any counter overshoots its target, this path is invalid/non-optimal
                if next_state_list[i] > target_tuple[i]:
                    is_valid_transition = False
                    break
            
            if not is_valid_transition:
                continue

            next_state = tuple(next_state_list)
            next_cost = current_cost + 1

            if next_state == target_tuple:
                # Found the target, since BFS guarantees shortest path (cost 1 per step)
                return next_cost
            
            # If the next state is new (no need to check for lower cost in BFS)
            if next_state not in min_presses:
                min_presses[next_state] = next_cost
                queue.append(next_state)

    # Should not happen if a solution exists
    return float('inf') 

def puzzle_2_solve(machines: List[Dict]) -> int:
    """Calculates the fewest total presses for all machines for Part 2."""
    total_presses = 0
    
    for machine in machines:
        target = machine['joltage_targets']
        buttons = machine['buttons']
        num_lights = len(target) # Note: For Part 2, this is num_counters
        num_buttons = len(buttons)
        
        if num_lights == 0 or num_buttons == 0:
            return float('inf')
            
        presses = solve_system_z_minimal_sum(num_lights, num_buttons, buttons, target)
        
        if presses == float('inf'):
            return float('inf')
            
        total_presses += presses
        
    return total_presses


# --- Main Execution ---

if __name__ == "__main__":
    start_time = time.perf_counter()
    
    # 1. Parse Input
    machines = parse_input('input.txt')
    
    # 2. Solve Puzzle 1
    p1_start = time.perf_counter()
    result_1 = puzzle_1_solve(machines)
    p1_duration = (time.perf_counter() - p1_start) * 1000

    # 3. Solve Puzzle 2
    p2_start = time.perf_counter()
    result_2 = puzzle_2_solve(machines)
    p2_duration = (time.perf_counter() - p2_start) * 1000
    
    total_duration = (time.perf_counter() - start_time) * 1000

    # 4. Display Results
    # Handling the 'inf' case if a machine is unsolvable
    if result_1 == float('inf') or result_2 == float('inf'):
        print("An impossible configuration was found. Results may be incorrect.")
        result_1 = "Unsolvable" if result_1 == float('inf') else result_1
        result_2 = "Unsolvable" if result_2 == float('inf') else result_2
        
    print(f"Puzzle 1: {result_1}")
    print(f"Puzzle 2: {result_2}")
    print(f"Total Duration: {total_duration:.2f}ms")