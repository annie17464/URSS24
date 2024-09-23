#2. Probabilistic Serial Mechanism

import numpy as np
import pandas as pd
import copy
from weighted_b_matching import WBbM

# Extract the preferences 
df_named = pd.read_csv('flatpref.csv')
df= df_named.drop(df_named.columns[0], axis=1)
df_original= copy.deepcopy(df) # Keep a copy of the original dataframe (without names)
print(df)

# Input block capacities 
def flat_capacities(N):
    capacities = []
    for i in range(N):  # Assuming there are N accommodation blocks
        capacity = int(input(f"Please enter the maximum capacity for block b{i+1}: "))
        capacities.append(capacity)
    return capacities

N = 6 # We have fixed N here, but it can be kept variable  
capacities = flat_capacities(N)
original_capacity= copy.deepcopy(capacities)
capacities = np.array(capacities).astype(float) # We keep capacities as a numpy array in floats as this format will be used for the SEA algorithm later

matrix = np.zeros(df.shape) # Initialising matrix to store output of SEA in

# Define a function to adjust the item preference orders after each round of consumption (i.e., when an item has been fully consumed)
def adjust_row(row):
    values = row.tolist()
    ranked_values = sorted(values, reverse=False) # We sort the old values of the rows
    new_values = []

    for value in values:
        rank = ranked_values.index(value) + 1  # Rank starts at 1
        new_values.append(rank if value > 0 else value)

    return pd.Series(new_values, index=row.index)

# Simultaneous Eating Algorithm 
while np.any(capacities > 0):
    # Count the number of 1s in each column- this is each student's top preference
    num_ones = (df == 1).sum(axis=0).values # This is the number of consumers of each item in a round 
    ratios = np.divide(capacities, num_ones, where=num_ones != 0, out=np.full_like(capacities, np.inf))

    # We use these ratios to identify the item with the highest rate of consumption, i.e., the one that will get exhausted first 
    min_col_idx = np.argmin(ratios)

    # The minimum value to be added
    min_value = ratios[min_col_idx]

    # Locate all positions with 1s in the original DataFrame
    ones_positions = df == 1

    # Check the maximum value we can add without exceeding capacity
    can_eat = min(min_value, capacities[min_col_idx])
    
    # Add the minimum value to all positions that have 1s in the original DataFrame
    matrix[ones_positions] += can_eat
    total_eaten = num_ones * min_value

    # Ensure capacities don't go negative
    capacities -= np.minimum(total_eaten, capacities)
    df.iloc[:, min_col_idx] = df.shape[1]+1
    df = df.apply(adjust_row, axis=1)

print("Final SEA fractional assignment:")
print(matrix)

# Function to verify the matrix is singly stochastic 
# Note that the matrix would be doubly stochastic if each item was getting assigned to only one person instead of non-unity capacities 
def verify_stochastic_matrix(matrix, original_capacity):
    # Check if every row sums to 1
    rows_valid = np.all(np.isclose(matrix.sum(axis=1), 1))
    
    # Check if every column sums to original capacities
    columns_valid = np.all(np.isclose(matrix.sum(axis=0), original_capacity))
    
    if rows_valid and columns_valid:
        return "Output verified - the matrix is singly stochastic"
    else:
        return "Verification failed - the matrix is not singly stochastic"

# Run verification
result = verify_stochastic_matrix(matrix, original_capacity)
print(result)

# Note: The above code finds the SEA matrix and verifies it. It can be used independently if an alternate method of decomposition is preferred 

fmatrix= copy.deepcopy(matrix) # Retaining a copy of the SEA output matrix

# Now, we want to find the convex hull decomposition of our SEA matrix in order to probabilistically choose an assignment
# We find its optimal assignment:
def components(matrix):
    preferences = matrix.tolist()
    W = matrix.ravel().tolist() 
    num_left = len(preferences)
    num_right = len(preferences[0])

    ldp = 0
    udp = original_capacity
    uda = 1
    lda = 1

    b_matching = WBbM(num_left, num_right, W, lda, uda, ldp, udp, LogToConsole=0)
    results, total_weight= b_matching.Bb_matching(optimization_mode="max")
    return results

# We subtract the highest multiple of the component matrices from the original matrix in order to obtain their coefficients in the decomposition (weights)
def birkhoff_von_neumann(matrix, max_iterations=6): # I have limited the iterations to 6 here, as the dataset is large. This is not necessary for smaller datasets
    n, m = matrix.shape
    component_matrices = []
    weights = []
    
    # Make a working copy of the matrix
    working_matrix = np.copy(matrix)
    iteration = 0  # Initialize iteration counter
    
    while np.any(working_matrix > 5e-2): 
        if iteration >= max_iterations:
            print(f"Maximum iterations ({max_iterations}) reached.")
            break
        
        c_matrix = components(working_matrix)
        
        # Compute the maximum weight we can subtract from the current matrix
        min_weight = np.inf        
        for i in range(n):
            for j in range(m):
                if c_matrix[i, j] == 1:
                    min_weight = min(min_weight, working_matrix[i, j])
                    
        # Update the working matrix by subtracting min weight
        working_matrix = working_matrix - (min_weight * c_matrix)
        
        # Store the permutation matrix and the corresponding weight
        component_matrices.append(c_matrix)
        weights.append(min_weight)        
        iteration += 1  # Increment iteration counter
    
    return component_matrices, weights

# Run the Birkhoff-von Neumann decomposition with a max iteration limit
component_matrices, weights = birkhoff_von_neumann(fmatrix, max_iterations=6)

print("\nDecomposition into permutation matrices and weights:\n") # We print the permutation (composition) matrices along with their weights
for i, (c_matrix, weight) in enumerate(zip(component_matrices, weights)):
    print(f"Permutation Matrix {i+1}:\n", c_matrix)
    print(f"Weight {i+1}: {weight}\n")

# We select one of the permutation matrices based on their weights 
sum_weights = np.sum(weights)

if sum_weights == 0 or np.isnan(sum_weights) or np.isinf(sum_weights):
    print("Error: sum of weights is zero, NaN, or infinite.")
else:
    normalised_weights = np.array(weights) / sum_weights # This is done so that we can select a matrix even if their weights do not sum to 1 

    if np.any(np.isnan(normalised_weights)):
        print("Error: Normalized weights contain NaN values.") 
    else:
        index = np.random.choice(len(component_matrices), p=normalised_weights)
        selected_matrix = component_matrices[index]
        probability = normalised_weights[index]
        print("Selected Allocation:")
        print(selected_matrix)
        print(f"with probability {probability}")

# Add preliminary accomodation column to dataframe for easy csv conversion 
column_headers = df_original.columns.tolist()

def find_preliminary_accommodation(row):
    col_index = np.argmax(row)
    return column_headers[col_index]
preliminary_accommodations = [find_preliminary_accommodation(row) for row in selected_matrix]
df_named['Preliminary Accommodation'] = preliminary_accommodations
print(df_named)

# Check how many people got their first preferences, second preferences and so on using PS algorithm
counts = np.zeros(6).astype(int)
for index, row in df_named.iterrows():
    prelim_accom = row['Preliminary Accommodation']    
    corresponding_entry = row[prelim_accom]    
    counts[corresponding_entry - 1] += 1

print(counts)
print(f"This algorithm gives {counts[0]} people their first preferences, {counts[1]} people their second preference, {counts[2]} people their third preference, and so on as given by the above array.")

# It is interesting to consider that the SEA matrix could provide more accurate weights to the weighted b-matching or hungarian algorithhms by ruling out unrealistic matchings. 
# We can therefore also compare the results of PSM, the ranks-as-weights hungarian algorithm and the SEA-weights hungarian algorithm by checking which preferences people got in the first optimal assignment of SEA matrix
counts1 = np.zeros(6, dtype=int)
headers= df_original.columns
optimal_matrix_post_SEA= component_matrices[0]
for i in range(optimal_matrix_post_SEA.shape[0]):
    index_of_one = np.argmax(optimal_matrix_post_SEA[i])
    selected_header = headers[index_of_one]
    value = df_original.loc[i, selected_header]
    counts1[value - 1] += 1

print(f"Directly choosing the optimal matrix after implementing SEA would have given us the array {counts1}")
