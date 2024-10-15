# This file contains a small incorporation of favourable variance in flats by dividing students into subgroups based on a feature
#(here, we have chosen football teams under the assumption "two football fans of the same team together make for a noisy/undesirable flat")
# these subgroups are taken up one by one and allocated houses based on their preferences for each house 

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas
from munkres import Munkres, print_matrix

df = pandas.read_csv('toydata.csv')
df_numeric = df.replace({'Yes': 0, 'No': 1}, inplace= False)
print(df)
print(df_numeric)

# Step 3: Calculate scores for each flat
df_numeric['flat_1'] = df_numeric['Social'] + df_numeric['Quiet hours']
df_numeric['flat_2'] = (1 - df_numeric['Social']) + df_numeric['Quiet hours']
df_numeric['flat_3'] = df_numeric['Social'] + (1 - df_numeric['Quiet hours'])
df_numeric['flat_4'] = 2 - df_numeric['Social'] - df_numeric['Quiet hours']
preferences = df_numeric[['flat_1', 'flat_2', 'flat_3', 'flat_4']].values

# Function to run the Munkres algorithm and format results
def run_munkres(team_name):
    m = Munkres()
    team_df = df_numeric[df['Team'] == team_name]
    cost_matrix = team_df[['flat_1', 'flat_2', 'flat_3', 'flat_4']].values
    print_matrix(cost_matrix, msg=f'The flat preferences of students supporting {team_name} are given by the matrix below: ')
    indexes = m.compute(cost_matrix)
    assignments = {}

    for row, column in indexes:
        flat = column + 1  # Flat number (1-indexed)
        names = team_df.iloc[row]['Name']  # Assuming 'Name' is the column with person names
        if flat not in assignments:
            assignments[flat] = []
        assignments[flat].append(names)
    
    return assignments

# Step 4: Run the algorithm for both teams
arsenal_assignments = run_munkres('Arsenal')
manchester_assignments = run_munkres('Man Utd')

# Step 5: Combine the results
combined_assignments = {}

def add_assignments(assignments):
    for flat, names in assignments.items():
        if flat not in combined_assignments:
            combined_assignments[flat] = []
        combined_assignments[flat].extend(names)

add_assignments(arsenal_assignments)
add_assignments(manchester_assignments)

# Step 6: Print the combined results
print('Our final flat allocation is given by: ')
for flat in sorted(combined_assignments.keys()):
    names = combined_assignments[flat]
    print(f"Flat {flat}: {', '.join(names)}")
