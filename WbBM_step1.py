# this file contains the solution for the first step of the problem, the block allocation, through the weighted b matching algorithm. 

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
from weighted_b_matching import WBbM

def output(df, allocations, output_file):
    df['Allocated Flat'] = allocations
    df.to_csv(output_file, index=False)

def flat_capacities(N):
    capacities = []
    for i in range(N):  # Assuming there are N accommodation blocks
        capacity = int(input(f"Please enter the maximum capacity for block b{i+1}: "))
        capacities.append(capacity)
    return capacities

if __name__ == "__main__":
    df = pd.read_csv('flatpref.csv')  # Read CSV and set the first column as index
    preferences = df.iloc[:, 1:].values.tolist()
    W = df.iloc[:, 1:].values.ravel().tolist()  # Exclude the first column and convert values to float
    num_left = len(preferences)
    num_right = len(preferences[0])

    N = num_right
    labels = [f'b{i+1}' for i in range(num_right)]

    row_capacity, column_capacity = [1]*num_left, [1]*num_right
    ldp = 0
    udp = flat_capacities(N)
    uda = 1
    lda = 1
     
    b_matching = WBbM(num_left, num_right, W, lda, uda, ldp, udp, LogToConsole=0)
    results, total_weight = b_matching.Bb_matching(optimization_mode="min") # Note that the optimization mode has been set to minimum here: that is because we consider 1 to be the most-preferred item
    print(results)

    allocations = [''] * num_left
    for row_index in range(len(results)):
        for column_index in range(len(results[row_index])):
            if results[row_index][column_index] == 1:
                allocations[row_index] = labels[column_index]

    df['Preliminary Accommodation'] = allocations
    print(df)
    output_file = 'preliminary_accommodations.csv'
    output(df, allocations, output_file)

# Check how many people got their first preferences, second preferences and so on using weighted b-matching algorithm
counts = np.zeros(6).astype(int)
# Iterate through each row of the dataframe
for index, row in df.iterrows():
    # Get the 'preliminary accommodation' value (which is 'b1', 'b2', etc.)
    prelim_accom = row['Preliminary Accommodation']
    # Access the corresponding entry in the column specified by 'preliminary accommodation'
    corresponding_entry = row[prelim_accom]    
    # Increment the corresponding count (subtract 1 to map 1-6 to indices 0-5)
    counts[corresponding_entry - 1] += 1

print(counts)
print(f"This algorithm gives {counts[0]} people their first preferences, {counts[1]} people their second preference, {counts[2]} people their third preference, and so on as given by the above array.")