from munkres import Munkres, print_matrix
# I am using a driver matrix, but we can easily make this an input matrix using the code snippet below:
def suitability_inputs(N):
    matrix = []
    
    for i in range(N):
        candidate = input(f"Please enter the suitability of candidate {i + 1} for each task (separated with spaces!): ")
        row = list(map(int, candidate.split()))
        matrix.append(row)
    print(matrix)
    # we allow edits to inputs:

    edit= input("Please enter Y to confirm input matrix, else enter N: ")
    if edit== "N":
        change_index= int(input("Which row number would you like to edit? "))
        input_row= input("Please enter your new row: ")
        change_row= list(map(int, input_row.split()))
        matrix[change_index -1]=  change_row
    return matrix

# execution: 
N = int(input("Please enter the number of candidates or positions taken into consideration: "))
matrix = suitability_inputs(N) 
''' 
# This is the driver matrix as presented in the manual of munkres
# I have added user inputs but commented it for reference 
matrix = [[5, 9, 1],
          [10, 3, 2],
          [8, 7, 4]] 
'''
m = Munkres()
indexes = m.compute(matrix)
print_matrix(matrix, msg='Suitability matrix: ')
print('The most suitable assignment is given by: ')
for row, column in indexes:
    print(f'({row}, {column})')
