#1. Randomized Algorithm: Random Serial Dictatorship (RSD)

import numpy as np
import random
import pandas as pd 
from itertools import chain

# Extract the user preferences from the csv file 
df = pd.read_csv('flatpref.csv')

# Input block capacities 
def flat_capacities(N):
    capacities = []
    for i in range(N):  # Assuming there are N accommodation blocks
        capacity = int(input(f"Please enter the maximum capacity for block b{i+1}: "))
        capacities.append(capacity)
    return capacities

N = 6 # We have fixed the number of blocks here- this can be changed accordingly 
capacities = flat_capacities(N)

# Generate a list of column indices to keep based on capacities
# Assumes that the columns are indexed from 0 to len(df.columns)-1
column_indices = range(len(df.columns))
L = list(chain.from_iterable([[i+1] * capacities[i] for i in column_indices if i < len(capacities)]))

# Ensure indices are within bounds
valid_indices = [idx for idx in L if 0 <= idx < len(df.columns)]

res = df.iloc[:, valid_indices]
print(res)
df_preferences = res.values
preferences = res.values.tolist()  # Convert the preferences dataframe to a list of lists

# Function to remove the chosen item from all participants' preferences
def remove_item_from_preferences(preferences, item_index):
    for pref in preferences:
        pref.pop(item_index)
    return preferences

# Random Serial Dictatorship function
def random_serial_dictatorship(participants, items, preferences):
    random.shuffle(participants)  # Randomize the order of participants
    allocation = {participant: None for participant in participants}
    
    for participant in participants:
        # Get the participant's index and their preferences
        participant_index = participants.index(participant)
        participant_preferences = preferences[participant_index]
        
        # Find the index of the most preferred available item
        preferred_item_index = participant_preferences.index(min(participant_preferences))
        
        # Allocate the most preferred item to the participant
        allocation[participant] = items[preferred_item_index]
        
        # Remove the chosen item from all participants' preference lists
        preferences = remove_item_from_preferences(preferences, preferred_item_index)
        
        # Remove the item from the list of items
        items.pop(preferred_item_index)
    
    return allocation

# List of participants' names (assuming the first column is 'Name')
participants = df['Name'].tolist()

# List of items (accommodation blocks)
items = list(res.columns)

# Running the Random Serial Dictatorship algorithm
allocation = random_serial_dictatorship(participants, items, preferences)

# Output the final allocation
print("1. Random Serial Dictatorship (RSD) Allocation:")
allocation_df = pd.DataFrame(list(allocation.items()), columns=['Name', 'Preliminary Accommodation'])
print(allocation_df)

# We can optionally sort the DataFrame in the original students' order:
allocation_df['Numeric_Part'] = allocation_df['Name'].str.extract('(\d+)').astype(int)
allocation_df_sort = allocation_df.sort_values(by='Numeric_Part').drop(columns='Numeric_Part')

# Output the sorted DataFrame
print("Sorted RSD Allocation:")
print(allocation_df_sort)

# Check how many people got their first preferences, second preferences and so on using RSD algorithm
headers = df.columns
counts = np.zeros(6, dtype=int)

for index, row in allocation_df_sort.iterrows():
    # Get the 'preliminary accommodation' value (which is 'b1', 'b2', etc.)
    prelim_accom = row['Preliminary Accommodation']
    
    # Access the corresponding entry in the column specified by 'preliminary accommodation'
    corresponding_entry = df.loc[index, prelim_accom]
    
    # Increment the corresponding count (subtract 1 to map 1-6 to indices 0-5)
    counts[corresponding_entry -1] += 1

print(counts)
print(f"This algorithm gives {counts[0]} people their first preferences, {counts[1]} people their second preference, {counts[2]} people their third preference, and so on as given by the above array.")