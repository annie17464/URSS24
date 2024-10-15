# This file contains the python code for the hungarian algorithm 
# to use deepcopy later, I import copy 
import copy

# to reduce our matrix to obtain the initial zeroes, we write smallest in rows and smallest in column functions 
def smallest_in_rows(matrix):
    return [min(row) for row in matrix]

def smallest_in_columns(matrix, N):
    return [min(matrix[i][j] for i in range(N)) for j in range(N)]

# we use these to reduce our matrix to one with atleast N zeroes
def reduce_matrix(matrix, N):
    row_mins = smallest_in_rows(matrix)
    reduced_matrix = []
    
    # we subtract the respective row minimum from each element in a row
    for i in range(N):
        reduced_row = [matrix[i][j] - row_mins[i] for j in range(N)]
        reduced_matrix.append(reduced_row)
    
    col_mins = smallest_in_columns(reduced_matrix, N)
    # we repeat this for columns
    for j in range(N):
        for i in range(N):
            reduced_matrix[i][j] -= col_mins[j]
    
    return reduced_matrix

# we count the number of zeroes in each row and each column in our matrix and store them in row0count_array and col0count_array
def zerocounts(matrix):
    row0count_array = [sum(1 for x in row if x == 0) for row in matrix]
    col0count_array = [sum(1 for row in matrix if row[j] == 0) for j in range(len(matrix[0]))]
    return row0count_array, col0count_array

# we now want to replace our entries in an entire specified row by -1
def replace_row(matrix, row_index):
    matrix[row_index] = [-1] * len(matrix[0])
    return matrix

# and similarly for the columns
def replace_column(matrix, col_index):
    for row in matrix:
        row[col_index] = -1
    return matrix

# if an entry belongs to a specific row and a specific column, we want it to have the value -1
# this will be used when we cross out our matrix to identify where our lines lie
def adjust_entries(matrix, removed_rows, removed_cols):
    for i in removed_rows:
        for j in removed_cols:
            matrix[i][j] = -2
    return matrix

# we define a function that establishes where we want to cross out elements of a matrix, and keeps a record of the affected rows and columns,
# replacing them appropriately
def iterative_crossing_out(matrix):
    removed_rows = []
    removed_cols = []
    row0count_array, col0count_array = zerocounts(matrix)
    # this is the total number of zeros in all columns and rows
    # note that double-counting does not affect us in this case as we only need the condition "while sumcount !=0"
    sumcount = sum(row0count_array + col0count_array)
    
    # we now replace our rows according to where the maximum number of zeroes lie, since to use minimum lines to cover all zeroes 
    # we would like to cover the maximum possible number of zeroes with each line
    # we also append our removed rows and columns simultaneously, as this will be used later 
    while sumcount != 0 and matrix:
        row0count_array, col0count_array = zerocounts(matrix)
        sumcount = sum(row0count_array + col0count_array)
        max_row_zeros = max(row0count_array)
        row_index = row0count_array.index(max_row_zeros)
        max_col_zeros = max(col0count_array)
        col_index = col0count_array.index(max_col_zeros)

        if max_row_zeros == 0 and max_col_zeros ==0:
            break
        # This is in case the number of zeroes of the rows and columns are the same. 
        # To determine which line to use, we count the number of rows and columns with max zeroes and compare
        if max_row_zeros == max_col_zeros:
            row_count = row0count_array.count(max_row_zeros)
            col_count = col0count_array.count(max_col_zeros)
            if row_count >= col_count:
                row_index = row0count_array.index(max_row_zeros)
                removed_rows.append(row_index)
                matrix = replace_row(matrix, row_index)
            else:
                col_index = col0count_array.index(max_col_zeros)
                removed_cols.append(col_index)
                matrix = replace_column(matrix, col_index)
        elif max_row_zeros > max_col_zeros:
            row_index = row0count_array.index(max_row_zeros)
            removed_rows.append(row_index)
            matrix = replace_row(matrix, row_index)
        else:
            removed_cols.append(col_index)
            matrix = replace_column(matrix, col_index)
        
        print(removed_rows, removed_cols)
        print(matrix)
    
    matrix = adjust_entries(matrix, removed_rows, removed_cols)
    print(matrix)
    return removed_rows, removed_cols, matrix

# we want to find the smallest element in the non crossed-out elements, that is, the elements that are not -1 or -2
# note that we have used the reduced matrix directly, as crossing out makes crossed elements negative. 
# by conditioning the smallest element to be positive, we can use the reduced matrix instead of the crossed out matrix 
def smallest_element(matrix):
    smallest = float('inf')

    for i in range(len(reduced)):
        for j in range(len(reduced[0])):
            if matrix[i][j] > 0 and matrix[i][j] < smallest:
                smallest = matrix[i][j]

    return smallest

# we now want to subtract this smallest element from the non crossed-out elements and add it to the doubly crossed out elements
# we leave the singly crossed-out elements as is
def subtract_minimum(matrix, reduced, removed_rows, removed_cols):
    smallest = smallest_element(matrix)
    updated_matrix = []

    for i in range(len(reduced)):
        updated_row = []
        for j in range(len(reduced[0])):
            if i in removed_rows and j in removed_cols:
                updated_entry = reduced[i][j] + smallest
            elif i not in removed_rows and j not in removed_cols:
                updated_entry = reduced[i][j] - smallest
            else:
                updated_entry = reduced[i][j]
            updated_row.append(updated_entry)
        updated_matrix.append(updated_row)
    
    return updated_matrix

# we want to find an assignment of zeroes such that each zero covers a unique row and column 
# this matches the candidate to the job 
def find_assignment(matrix):
    n = len(matrix)
    rows_matched = [-1] * n
    cols_matched = [-1] * n
    assignments = []
    
    def can_assign(row, used, rows_matched, cols_matched):
        for col in range(n):
            if matrix[row][col] == 0 and not used[col]:
                used[col] = True
                if cols_matched[col] == -1 or can_assign(cols_matched[col], used, rows_matched, cols_matched):
                    rows_matched[row] = col
                    cols_matched[col] = row
                    return True
        return False
    
    for row in range(n):
        used = [False] * n
        can_assign(row, used, rows_matched, cols_matched)
    
    for row in range(n):
        if rows_matched[row] != -1:
            assignments.append((row, rows_matched[row]))
    
    return assignments

# we want to loop this until we have found a suitable assignment, i.e., everyone gets a job. we hence introduce a main function
def main(matrix, reduced):    
    assignments = find_assignment(matrix)
    # and place our single-use assignment finder inside a while loop
    while len(assignments)< len(matrix) and assignments != []:
        # note: I have additionally printed steps necessary to check each part, these are not necessary for the algorithm
        print(reduced)
        removed_rows, removed_cols, matrix = iterative_crossing_out(matrix)
        print("Removed rows and columns after iterative crossing out:")
        print(removed_rows, removed_cols)
        
        smallest = smallest_element(matrix)
        print("Smallest element in uncovered rows and columns:")
        print(smallest)
        
        updated_matrix = subtract_minimum(matrix, reduced, removed_rows, removed_cols)
        print("Updated matrix after subtracting the minimum:")
        print(updated_matrix)

        assignments = find_assignment(updated_matrix)
        print("Final Assignment: ")
        print(assignments)
        
        # to ensure looping, we need to update our matrices for the next round
        # we use a deep copy so that the matrices can be modified independently of each other
        reduced= copy.deepcopy(updated_matrix)
        matrix = updated_matrix 

    # this is just the formatting of the final output!
    print("Candidate",  "Job")
    for candidate, job in assignments:
        print(f"{candidate + 1} \t {job + 1}")

# this is the user input function- we can input our own matrices for each calculation instead of a driver matrix
def suitability_inputs(N):
    matrix = []
    
    for i in range(N):
        candidate = input(f"Please enter the suitability of candidate {i + 1} for each task (separated with spaces!): ")
        row = list(map(int, candidate.split()))
        matrix.append(row)
    print(matrix)
    
# if someone has mistyped a row, we can allow edits. 
# Note that this function is currently only allowing one row to be edited, but this can be extended if required 
    edit= input("Please enter Y to confirm input matrix, else enter N: ")
    if edit== "N":
        change_index= int(input("Which row number would you like to edit? "))
        input_row= input("Please enter your new row: ")
        change_row= list(map(int, input_row.split()))
        matrix[change_index -1]=  change_row
        
    return matrix

# execution: 

# N gives us the dimension of our matrix, we can pull this into the input as well
# our inputs therefore are:
N = int(input("Please enter the number of candidates or positions taken into consideration: "))
matrix = suitability_inputs(N)

# we keep a copy of our original matrix: 
original = copy.deepcopy(matrix)
print("The original matrix is given by:")
for row in matrix:
    print(row)

# we reduce our matrix
reduced_matrix = reduce_matrix(matrix, N)

# since we now only need to work with our reduced matrix, we can keep both "matrix" and "reduced" as two individual copies of the reduced matrix
matrix = copy.deepcopy(reduced_matrix)
reduced = copy.deepcopy(matrix)
print("Reduced matrix:")
for row in reduced:
    print(row)
    
print("Running repetition until a suitable assignment is found:")

# we run our main function on the reduced matrix! 
main(matrix, reduced)
