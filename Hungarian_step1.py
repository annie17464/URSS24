# this file contains the solution for the first step of the problem, the block allocation, through the hungarian algorithm. 

import pandas as pd 
from itertools import chain
import numpy as np
from munkres import Munkres, print_matrix

# Extract the preferences
df = pd.read_csv('flatpref.csv')

def output(df, allocations, output_file):
    df['Allocated Flat'] = allocations
    df.to_csv(output_file, index=False)

def flat_capacities(N):
    capacities = []
    for i in range(N):  # Assuming there are N accommodation blocks
        capacity = int(input(f"Please enter the maximum capacity for block b{i+1}: "))
        capacities.append(capacity)
    return capacities

N = 6 # We have fixed N here, but it can be kept variable 
capacities = flat_capacities(N)

# Generate a list of column indices to keep based on capacities
# Assumes that the columns are indexed from 0 to len(df.columns)-1
column_indices = range(len(df.columns))
L = list(chain.from_iterable([[i+1] * capacities[i] for i in column_indices if i < len(capacities)]))

# Ensure indices are within bounds
valid_indices = [idx for idx in L if 0 <= idx < len(df.columns)]

# We store multiple copies of each row in a new dataframe- "preferences"- according to capacities
res = df.iloc[:, valid_indices]
print(res)
preferences = res.values
print(preferences)

# We run the hungarian algorithm
m = Munkres() # This is the Munkres package for the hungarian algorithm
cost_matrix = preferences
indexes = m.compute(cost_matrix)
headers= list(res.columns)
allocations = [headers[col] for row, col in indexes]

# Add the allocations as a new column in the DataFrame
df['Preliminary Accommodation'] = allocations

# Print results
print("Updated DataFrame with Preliminary Accommodation:")
print(df)
output_file = 'preliminary_accommodations.csv'
output(df, allocations, output_file)

# Check how many people got their first preferences, second preferences and so on using the hungarian algorithm
counts = np.zeros(6).astype(int)

# Iterate through each row of the dataframe
for index, row in df.iterrows():
    prelim_accom = row['Preliminary Accommodation']
    corresponding_entry = row[prelim_accom]
    counts[corresponding_entry - 1] += 1

print(counts)
print(f"This algorithm gives {counts[0]} people their first preferences, {counts[1]} people their second preference, {counts[2]} people their third preference, and so on as given by the above array.")